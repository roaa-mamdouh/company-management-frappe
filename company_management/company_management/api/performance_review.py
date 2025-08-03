import frappe
from frappe import _
from company_management.company_management.auth.security import require_permission, filter_by_user_company

@frappe.whitelist(allow_guest=False, methods=['POST'])
@require_permission("Performance Review", "create")
def create_performance_review():
    """Create new performance review"""
    try:
        data = frappe.local.form_dict
        review = frappe.new_doc('Performance Review')
        review.update(data)
        review.insert()
        return {"success": True, "data": review.as_dict()}
    except Exception as e:
        frappe.log_error(f"Error creating performance review: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['GET'])
@require_permission("Performance Review", "read")
def get_performance_reviews():
    """Get all performance reviews"""
    try:
        # Filter by user's company through employee
        user_company = frappe.get_value("User Account", 
                                       {"email_address": frappe.session.user}, 
                                       "company")
        
        filters = {}
        if user_company and "Company Admin" not in frappe.get_roles():
            # Get employees from user's company
            company_employees = frappe.get_all('Employee', 
                                             filters={'company': user_company},
                                             pluck='name')
            if company_employees:
                filters['employee'] = ['in', company_employees]
        
        reviews = frappe.get_all('Performance Review',
                               filters=filters,
                               fields=['name', 'employee', 'review_period_start', 'review_period_end',
                                      'reviewer', 'overall_rating', 'workflow_state', 'review_date'])
        return {"success": True, "data": reviews}
    except Exception as e:
        frappe.log_error(f"Error fetching performance reviews: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['GET'])
@require_permission("Performance Review", "read")
def get_performance_review(name):
    """Get single performance review"""
    try:
        review = frappe.get_doc('Performance Review', name)
        return {"success": True, "data": review.as_dict()}
    except Exception as e:
        frappe.log_error(f"Error fetching performance review {name}: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['PATCH'])
@require_permission("Performance Review", "write")
def update_performance_review(name):
    """Update existing performance review"""
    try:
        data = frappe.local.form_dict
        review = frappe.get_doc('Performance Review', name)
        review.update(data)
        review.save()
        return {"success": True, "data": review.as_dict()}
    except Exception as e:
        frappe.log_error(f"Error updating performance review {name}: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['POST'])
@require_permission("Performance Review", "submit")
def submit_performance_review(name):
    """Submit performance review"""
    try:
        review = frappe.get_doc('Performance Review', name)
        review.submit()
        return {"success": True, "data": review.as_dict()}
    except Exception as e:
        frappe.log_error(f"Error submitting performance review {name}: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['GET'])
@require_permission("Performance Review", "read")
def get_reviews_by_employee(employee):
    """Get performance reviews for specific employee"""
    try:
        reviews = frappe.get_all('Performance Review',
                               filters={'employee': employee},
                               fields=['name', 'review_period_start', 'review_period_end',
                                      'reviewer', 'overall_rating', 'workflow_state'],
                               order_by='review_period_end desc')
        return {"success": True, "data": reviews}
    except Exception as e:
        frappe.log_error(f"Error fetching reviews for employee {employee}: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['GET'])
@require_permission("Performance Review", "read")
def get_pending_reviews():
    """Get pending performance reviews for current user"""
    try:
        # Get reviews where current user is the reviewer
        user_email = frappe.session.user
        employee_name = frappe.get_value('Employee', {'email_address': user_email}, 'name')
        
        if not employee_name:
            return {"success": True, "data": []}
        
        pending_reviews = frappe.get_all('Performance Review',
                                       filters={
                                           'reviewer': employee_name,
                                           'workflow_state': ['in', ['Pending Review', 'Review Scheduled', 'Under Approval']]
                                       },
                                       fields=['name', 'employee', 'review_period_start', 'review_period_end',
                                              'workflow_state', 'review_date'])
        return {"success": True, "data": pending_reviews}
    except Exception as e:
        frappe.log_error(f"Error fetching pending reviews: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['POST'])
def workflow_action(name, action):
    """Execute workflow action on performance review"""
    try:
        review = frappe.get_doc('Performance Review', name)
        
        # Validate workflow action based on current state and user role
        user_roles = frappe.get_roles()
        current_state = review.workflow_state
        
        # Define valid actions according to Employee Performance Review Cycle workflow
        valid_actions = {
            "Pending Review": {"Schedule Review": ["Department Manager", "Company Admin"]},
            "Review Scheduled": {"Provide Feedback": ["Department Manager", "Company Admin"]},
            "Feedback Provided": {"Submit for Approval": ["Department Manager"]},
            "Under Approval": {
                "Approve Review": ["Company Admin"],
                "Reject Review": ["Company Admin"]
            },
            "Review Rejected": {"Update Feedback": ["Department Manager"]}
        }
        
        if current_state in valid_actions and action in valid_actions[current_state]:
            allowed_roles = valid_actions[current_state][action]
            if any(role in user_roles for role in allowed_roles):
                # Set flag to prevent automatic transitions during manual workflow actions
                frappe.flags.in_workflow_action = True
                
                try:
                    # Execute the workflow action according to Employee Performance Review Cycle
                    if action == "Schedule Review":
                        review.workflow_state = "Review Scheduled"
                    elif action == "Provide Feedback":
                        review.workflow_state = "Feedback Provided"
                    elif action == "Submit for Approval":
                        review.workflow_state = "Under Approval"
                        review.submitted_for_approval = 1
                    elif action == "Approve Review":
                        review.workflow_state = "Review Approved"
                        review.submit()
                    elif action == "Reject Review":
                        review.workflow_state = "Review Rejected"
                    elif action == "Update Feedback":
                        review.workflow_state = "Feedback Provided"
                    
                    review.save()
                    return {"success": True, "data": review.as_dict()}
                    
                finally:
                    # Clear the flag
                    frappe.flags.in_workflow_action = False
            else:
                return {"success": False, "error": "Insufficient permissions for this action"}
        else:
            return {"success": False, "error": "Invalid action for current state"}
            
    except Exception as e:
        frappe.log_error(f"Error executing workflow action {action} on {name}: {str(e)}")
        return {"success": False, "error": str(e)}