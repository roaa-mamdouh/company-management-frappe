import frappe
import unittest

class TestWorkflow(unittest.TestCase):
    def setUp(self):
        # Create test company
        self.company = frappe.get_doc({
            "doctype": "CM Company",
            "company_name": "Test Company for Workflow"
        })
        self.company.insert()
        
        # Create test department
        self.department = frappe.get_doc({
            "doctype": "CM Department",
            "department_name": "Test Department for Workflow",
            "company": self.company.name
        })
        self.department.insert()
        
        # Create test employee
        self.employee = frappe.get_doc({
            "doctype": "CM Employee",
            "employee_name": "Test Employee Workflow",
            "email_address": "test.employee@workflow.com",
            "company": self.company.name,
            "department": self.department.name
        })
        self.employee.insert()
        
        # Create test reviewer
        self.reviewer = frappe.get_doc({
            "doctype": "CM Employee",
            "employee_name": "Test Reviewer Workflow",
            "email_address": "test.reviewer@workflow.com",
            "company": self.company.name,
            "department": self.department.name
        })
        self.reviewer.insert()
        
        # Create performance review for workflow testing
        self.review = frappe.get_doc({
            "doctype": "Performance Review",
            "employee": self.employee.name,
            "reviewer": self.reviewer.name,
            "review_period_start": "2024-01-01",
            "review_period_end": "2024-12-31",
            "workflow_state": "Pending Review"
        })
        self.review.insert()
    
    def test_workflow_states(self):
        """Test all workflow states are valid"""
        valid_states = [
            "Pending Review",
            "Review Scheduled", 
            "Feedback Provided",
            "Under Approval",
            "Review Approved",
            "Review Rejected"
        ]
        
        for state in valid_states:
            self.review.workflow_state = state
            self.review.save()
            self.assertEqual(self.review.workflow_state, state)
    
    def test_workflow_transition_pending_to_scheduled(self):
        """Test transition from Pending Review to Review Scheduled"""
        self.review.workflow_state = "Pending Review"
        self.review.save()
        
        # Simulate scheduling review
        self.review.workflow_state = "Review Scheduled"
        self.review.review_date = "2025-02-01"
        self.review.save()
        
        self.assertEqual(self.review.workflow_state, "Review Scheduled")
        self.assertIsNotNone(self.review.review_date)
    
    def test_workflow_transition_scheduled_to_feedback(self):
        """Test transition from Review Scheduled to Feedback Provided"""
        self.review.workflow_state = "Review Scheduled"
        self.review.save()
        
        # Provide feedback
        self.review.feedback = "Employee shows good technical skills"
        self.review.overall_rating = "4 - Good"
        self.review.workflow_state = "Feedback Provided"
        self.review.save()
        
        self.assertEqual(self.review.workflow_state, "Feedback Provided")
        self.assertIsNotNone(self.review.feedback)
        self.assertIsNotNone(self.review.overall_rating)
    
    def test_workflow_transition_feedback_to_approval(self):
        """Test transition from Feedback Provided to Under Approval"""
        self.review.workflow_state = "Feedback Provided"
        self.review.feedback = "Good performance overall"
        self.review.save()
        
        # Submit for approval
        self.review.submitted_for_approval = 1
        self.review.workflow_state = "Under Approval"
        self.review.save()
        
        self.assertEqual(self.review.workflow_state, "Under Approval")
        self.assertEqual(self.review.submitted_for_approval, 1)
    
    def test_workflow_transition_approval_to_approved(self):
        """Test transition from Under Approval to Review Approved"""
        self.review.workflow_state = "Under Approval"
        self.review.feedback = "Excellent work throughout the year"
        self.review.overall_rating = "5 - Excellent"
        self.review.save()
        
        # Approve review
        self.review.workflow_state = "Review Approved"
        self.review.save()
        
        self.assertEqual(self.review.workflow_state, "Review Approved")
    
    def test_workflow_transition_approval_to_rejected(self):
        """Test transition from Under Approval to Review Rejected"""
        self.review.workflow_state = "Under Approval"
        self.review.save()
        
        # Reject review
        self.review.workflow_state = "Review Rejected"
        self.review.save()
        
        self.assertEqual(self.review.workflow_state, "Review Rejected")
    
    def test_workflow_transition_rejected_to_feedback(self):
        """Test transition from Review Rejected back to Feedback Provided"""
        self.review.workflow_state = "Review Rejected"
        self.review.save()
        
        # Update feedback and resubmit
        self.review.feedback = "Updated feedback with more details"
        self.review.workflow_state = "Feedback Provided"
        self.review.save()
        
        self.assertEqual(self.review.workflow_state, "Feedback Provided")
    
    def test_workflow_state_persistence(self):
        """Test that workflow state persists after reload"""
        original_state = "Feedback Provided"
        self.review.workflow_state = original_state
        self.review.save()
        
        # Reload from database
        self.review.reload()
        self.assertEqual(self.review.workflow_state, original_state)
    
    def test_workflow_required_fields(self):
        """Test that required fields are present for workflow"""
        # Employee is required
        self.assertIsNotNone(self.review.employee)
        
        # Reviewer is required
        self.assertIsNotNone(self.review.reviewer)
        
        # Review period dates are required
        self.assertIsNotNone(self.review.review_period_start)
        self.assertIsNotNone(self.review.review_period_end)
    
    def test_workflow_field_dependencies(self):
        """Test field dependencies based on workflow state"""
        # When in "Feedback Provided" state, feedback should be present
        self.review.workflow_state = "Feedback Provided"
        self.review.feedback = "Performance feedback provided"
        self.review.save()
        
        self.assertEqual(self.review.workflow_state, "Feedback Provided")
        self.assertIsNotNone(self.review.feedback)
        
        # When submitted for approval, flag should be set
        self.review.workflow_state = "Under Approval"
        self.review.submitted_for_approval = 1
        self.review.save()
        
        self.assertEqual(self.review.submitted_for_approval, 1)
    
    def tearDown(self):
        # Clean up test data
        try:
            frappe.delete_doc("Performance Review", self.review.name)
            frappe.delete_doc("CM Employee", self.employee.name)
            frappe.delete_doc("CM Employee", self.reviewer.name)
            frappe.delete_doc("CM Department", self.department.name)
            frappe.delete_doc("CM Company", self.company.name)
        except:
            pass