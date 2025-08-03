import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, getdate

class CMEmployee(Document):
    def before_save(self):
        self.calculate_days_employed()
    
    def calculate_days_employed(self):
        if self.hired_on:
            self.days_employed = date_diff(getdate(), self.hired_on)
    
    def on_update(self):
        # Update department and company counts
        if self.department:
            dept_doc = frappe.get_doc('CM Department', self.department)
            dept_doc.calculate_counts()
            dept_doc.save()