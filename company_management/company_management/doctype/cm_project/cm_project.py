import frappe
from frappe.model.document import Document

class CMProject(Document):
    def validate(self):
        self.validate_dates()
        self.validate_employees()
    
    def validate_dates(self):
        if self.end_date and self.start_date:
            if self.end_date < self.start_date:
                frappe.throw("End date cannot be before start date")
    
    def validate_employees(self):
        # Validate that assigned employees belong to the same company
        if self.assigned_employees:
            for emp in self.assigned_employees:
                employee = frappe.get_doc('CM Employee', emp.employee)
                if employee.company != self.company:
                    frappe.throw(f"Employee {emp.employee} does not belong to company {self.company}")