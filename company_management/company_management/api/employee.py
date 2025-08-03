import frappe
from frappe import _
from company_management.company_management.auth.security import require_permission, filter_by_user_company

@frappe.whitelist(allow_guest=False, methods=['POST'])
@require_permission("Employee", "create")
def create_employee():
    """Create new employee"""
    try:
        data = frappe.local.form_dict
        employee = frappe.new_doc('Employee')
        employee.update(data)
        employee.insert()
        return {"success": True, "data": employee.as_dict()}
    except Exception as e:
        frappe.log_error(f"Error creating employee: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['GET'])
@require_permission("Employee", "read")
def get_employees():
    """Get all employees"""
    try:
        filters = filter_by_user_company("Employee")
        employees = frappe.get_all('Employee', 
                                 filters=filters,
                                 fields=['name', 'employee_name', 'email_address', 
                                        'company', 'department', 'designation',
                                        'phone_number', 'status', 'hired_on', 'days_employed'])
        return {"success": True, "data": employees}
    except Exception as e:
        frappe.log_error(f"Error fetching employees: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['GET'])
@require_permission("Employee", "read")
def get_employee(name):
    """Get single employee"""
    try:
        employee = frappe.get_doc('Employee', name)
        return {"success": True, "data": employee.as_dict()}
    except Exception as e:
        frappe.log_error(f"Error fetching employee {name}: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['PATCH'])
@require_permission("Employee", "write")
def update_employee(name):
    """Update existing employee"""
    try:
        data = frappe.local.form_dict
        employee = frappe.get_doc('Employee', name)
        employee.update(data)
        employee.save()
        return {"success": True, "data": employee.as_dict()}
    except Exception as e:
        frappe.log_error(f"Error updating employee {name}: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['DELETE'])
@require_permission("Employee", "delete")
def delete_employee(name):
    """Delete employee"""
    try:
        frappe.delete_doc('Employee', name)
        return {"success": True, "message": "Employee deleted successfully"}
    except Exception as e:
        frappe.log_error(f"Error deleting employee {name}: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['GET'])
@require_permission("Employee", "read")
def get_employees_by_department(department):
    """Get employees by department"""
    try:
        filters = filter_by_user_company("Employee", {"department": department})
        employees = frappe.get_all('Employee',
                                 filters=filters,
                                 fields=['name', 'employee_name', 'email_address', 
                                        'designation', 'status'])
        return {"success": True, "data": employees}
    except Exception as e:
        frappe.log_error(f"Error fetching employees for department {department}: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['GET'])
@require_permission("Employee", "read")
def get_employee_performance_summary(name):
    """Get employee performance review summary"""
    try:
        employee = frappe.get_doc('Employee', name)
        
        # Get performance reviews
        reviews = frappe.get_all('Performance Review',
                               filters={'employee': name},
                               fields=['name', 'review_period_start', 'review_period_end',
                                      'overall_rating', 'workflow_state'],
                               order_by='review_period_end desc')
        
        return {
            "success": True, 
            "data": {
                "employee": employee.as_dict(),
                "performance_reviews": reviews
            }
        }
    except Exception as e:
        frappe.log_error(f"Error fetching performance summary for {name}: {str(e)}")
        return {"success": False, "error": str(e)}