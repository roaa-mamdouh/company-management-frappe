import frappe

def create_employee_performance_review_workflow():
    """Create the Employee Performance Review Cycle workflow with exact requirements"""
    workflow_name = "Employee Performance Review Cycle"
    
    try:
        # Delete existing workflow if it exists
        if frappe.db.exists("Workflow", workflow_name):
            frappe.delete_doc("Workflow", workflow_name)
            frappe.db.commit()
        
        # Create new workflow
        workflow = frappe.new_doc("Workflow")
        workflow.workflow_name = workflow_name
        workflow.document_type = "Performance Review"
        workflow.workflow_state_field = "workflow_state"
        workflow.is_active = 1
        workflow.send_email_alert = 1
        
        # Define workflow states according to requirements
        workflow_states = [
            {
                "state": "Pending Review",
                "doc_status": "0",
                "allow_edit": "System Manager",
                "style": "Warning"
            },
            {
                "state": "Review Scheduled", 
                "doc_status": "0",
                "allow_edit": "System Manager",
                "style": "Info"
            },
            {
                "state": "Feedback Provided",
                "doc_status": "0", 
                "allow_edit": "System Manager",
                "style": "Primary"
            },
            {
                "state": "Under Approval",
                "doc_status": "0",
                "allow_edit": "System Manager",
                "style": "Warning"
            },
            {
                "state": "Review Approved",
                "doc_status": "1",
                "allow_edit": "System Manager",
                "style": "Success"
            },
            {
                "state": "Review Rejected",
                "doc_status": "0",
                "allow_edit": "System Manager", 
                "style": "Danger"
            }
        ]
        
        # Add states to workflow
        for state in workflow_states:
            workflow.append("states", state)
        
        # Define workflow transitions according to requirements
        workflow_transitions = [
            {
                "state": "Pending Review",
                "action": "Schedule Review",
                "next_state": "Review Scheduled",
                "allowed": "System Manager",
                "condition": "",
                "allow_self_approval": 0
            },
            {
                "state": "Review Scheduled", 
                "action": "Provide Feedback",
                "next_state": "Feedback Provided",
                "allowed": "System Manager",
                "condition": "",
                "allow_self_approval": 0
            },
            {
                "state": "Feedback Provided",
                "action": "Submit for Approval", 
                "next_state": "Under Approval",
                "allowed": "System Manager",
                "condition": "",
                "allow_self_approval": 0
            },
            {
                "state": "Under Approval",
                "action": "Approve Review",
                "next_state": "Review Approved", 
                "allowed": "System Manager",
                "condition": "",
                "allow_self_approval": 0
            },
            {
                "state": "Under Approval",
                "action": "Reject Review",
                "next_state": "Review Rejected",
                "allowed": "System Manager", 
                "condition": "",
                "allow_self_approval": 0
            },
            {
                "state": "Review Rejected",
                "action": "Update Feedback",
                "next_state": "Feedback Provided",
                "allowed": "System Manager",
                "condition": "",
                "allow_self_approval": 0
            }
        ]
        
        # Add transitions to workflow
        for transition in workflow_transitions:
            workflow.append("transitions", transition)
        
        # Insert the workflow
        workflow.insert()
        frappe.db.commit()
        
        print(f"Successfully created workflow: {workflow.name}")
        return workflow
        
    except Exception as e:
        print(f"Error creating Employee Performance Review Cycle workflow: {str(e)}")
        frappe.log_error(f"Workflow Creation Error: {str(e)}")
        return None

def setup_workflow_notifications():
    """Setup email notifications for workflow transitions"""
    notifications = [
        {
            "subject": "Performance Review Scheduled",
            "document_type": "Performance Review",
            "event": "Value Change",
            "value_changed": "workflow_state",
            "condition": "doc.workflow_state == 'Review Scheduled'",
            "recipients": [
                {"receiver_by_document_field": "employee"}
            ],
            "message": "Your performance review has been scheduled."
        },
        {
            "subject": "Performance Review Feedback Provided",
            "document_type": "Performance Review", 
            "event": "Value Change",
            "value_changed": "workflow_state",
            "condition": "doc.workflow_state == 'Feedback Provided'",
            "recipients": [
                {"receiver_by_document_field": "employee"}
            ],
            "message": "Feedback has been provided for your performance review."
        },
        {
            "subject": "Performance Review Approved",
            "document_type": "Performance Review",
            "event": "Value Change", 
            "value_changed": "workflow_state",
            "condition": "doc.workflow_state == 'Review Approved'",
            "recipients": [
                {"receiver_by_document_field": "employee"},
                {"receiver_by_document_field": "reviewer"}
            ],
            "message": "Performance review has been approved."
        },
        {
            "subject": "Performance Review Rejected",
            "document_type": "Performance Review",
            "event": "Value Change",
            "value_changed": "workflow_state", 
            "condition": "doc.workflow_state == 'Review Rejected'",
            "recipients": [
                {"receiver_by_document_field": "reviewer"}
            ],
            "message": "Performance review has been rejected and needs revision."
        }
    ]
    
    for notification_data in notifications:
        if not frappe.db.exists("Notification", {"subject": notification_data["subject"]}):
            notification = frappe.new_doc("Notification")
            notification.update(notification_data)
            notification.insert()