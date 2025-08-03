import frappe
import unittest

class TestCompany(unittest.TestCase):
    def setUp(self):
        # Create test company
        self.company = frappe.get_doc({
            "doctype": "CM Company",
            "company_name": "Test Company Ltd",
            "description": "Test company for unit tests",
            "email": "test@testcompany.com",
            "phone": "+1-555-TEST"
        })
        self.company.insert()
    
    def test_company_creation(self):
        self.assertEqual(self.company.company_name, "Test Company Ltd")
        self.assertEqual(self.company.number_of_departments, 0)
        self.assertEqual(self.company.number_of_employees, 0)
        self.assertEqual(self.company.number_of_projects, 0)
    
    def test_department_count_calculation(self):
        # Create test department
        dept = frappe.get_doc({
            "doctype": "CM Department",
            "department_name": "Test Department",
            "company": self.company.name,
            "description": "Test department"
        })
        dept.insert()
        
        # Reload company and check count
        self.company.reload()
        self.company.calculate_counts()
        self.assertEqual(self.company.number_of_departments, 1)
        
        # Clean up
        frappe.delete_doc("CM Department", dept.name)
    
    def test_employee_count_calculation(self):
        # Create test department first
        dept = frappe.get_doc({
            "doctype": "CM Department", 
            "department_name": "Test Dept for Employee",
            "company": self.company.name
        })
        dept.insert()
        
        # Create test employee
        emp = frappe.get_doc({
            "doctype": "CM Employee",
            "employee_name": "Test Employee",
            "email_address": "test.employee@testcompany.com",
            "company": self.company.name,
            "department": dept.name
        })
        emp.insert()
        
        # Reload company and check count
        self.company.reload()
        self.company.calculate_counts()
        self.assertEqual(self.company.number_of_employees, 1)
        
        # Clean up
        frappe.delete_doc("CM Employee", emp.name)
        frappe.delete_doc("CM Department", dept.name)
    
    def tearDown(self):
        # Clean up test data
        try:
            frappe.delete_doc("CM Company", self.company.name)
        except:
            pass