import frappe
from frappe.model.document import Document

class CMCompany(Document):
    def before_save(self):
        self.calculate_counts()
    
    def calculate_counts(self):
        # Auto-calculate number of departments
        self.number_of_departments = frappe.db.count('CM Department', 
                                                    filters={'company': self.name})
        
        # Auto-calculate number of employees
        self.number_of_employees = frappe.db.count('CM Employee', 
                                                 filters={'company': self.name})
        
        # Auto-calculate number of projects
        self.number_of_projects = frappe.db.count('CM Project', 
                                                filters={'company': self.name})