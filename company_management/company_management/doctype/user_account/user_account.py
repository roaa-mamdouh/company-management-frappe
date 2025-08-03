import frappe
from frappe.model.document import Document

class UserAccount(Document):
    def validate(self):
        # Custom validation logic
        self.validate_email()
        self.set_role_permissions()
    
    def validate_email(self):
        if not frappe.utils.validate_email_address(self.email_address):
            frappe.throw("Invalid email address")
    
    def set_role_permissions(self):
        # Set default role based on user type
        if not self.role and self.user_type:
            if self.user_type == "Admin":
                self.role = "Company Admin"
            elif self.user_type == "Manager":
                self.role = "Department Manager"
            else:
                self.role = "Employee User"