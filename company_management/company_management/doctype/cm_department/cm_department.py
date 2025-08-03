import frappe
from frappe.model.document import Document

class CMDepartment(Document):
    def before_save(self):
        self.calculate_counts()
    
    def calculate_counts(self):
        # Auto-calculate number of employees
        self.number_of_employees = frappe.db.count('CM Employee', 
                                                 filters={'department': self.name})
        
        # Auto-calculate number of projects
        self.number_of_projects = frappe.db.count('CM Project', 
                                                filters={'department': self.name})
    
    def on_update(self):
        # Update company counts when department changes
        if self.company:
            company_doc = frappe.get_doc('CM Company', self.company)
            company_doc.calculate_counts()
            company_doc.save()