import frappe
from frappe.model.document import Document

class PerformanceReview(Document):
    def validate(self):
        self.check_automatic_transitions()
    
    def on_update(self):
        self.check_automatic_transitions()
    
    def on_update_after_submit(self):
        self.check_automatic_transitions()
    
    def check_automatic_transitions(self):
        """Check and execute automatic workflow transitions based on field changes"""
        # Skip automatic transitions if this is a workflow action
        if frappe.flags.in_workflow_action:
            return
            
        old_state = self.get_db_value('workflow_state') or self.workflow_state
        new_state = self.determine_new_workflow_state()
        
        if new_state and new_state != old_state:
            self.workflow_state = new_state
            frappe.msgprint(f"Workflow automatically transitioned to: {new_state}")
    
    def determine_new_workflow_state(self):
        """Determine the new workflow state based on current field values"""
        current_state = self.workflow_state
        
        # Pending Review → Review Scheduled: When review_date is set
        if current_state == "Pending Review" and self.review_date:
            return "Review Scheduled"
        
        # Review Scheduled → Feedback Provided: When feedback is recorded
        elif current_state == "Review Scheduled" and self.feedback:
            return "Feedback Provided"
        
        # Feedback Provided → Under Approval: When submitted_for_approval is checked
        elif current_state == "Feedback Provided" and self.submitted_for_approval:
            return "Under Approval"
        
        # Note: Under Approval → Review Approved/Rejected transitions are handled by manager actions
        # Review Rejected → Feedback Provided: When feedback is updated after rejection
        elif current_state == "Review Rejected" and self.feedback_updated_after_rejection():
            return "Feedback Provided"
        
        return None
    
    def feedback_updated_after_rejection(self):
        """Check if feedback was updated after rejection"""
        if self.workflow_state == "Review Rejected":
            # Check if any feedback fields have been changed using frappe's change detection
            feedback_fields = ['feedback', 'goals_achievements', 'areas_for_improvement', 'development_plan']
            
            for field in feedback_fields:
                if self.has_value_changed(field):
                    return True
            
        return False