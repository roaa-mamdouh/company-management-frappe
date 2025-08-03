import frappe
import unittest
from frappe.utils import getdate, date_diff

class TestEmployee(unittest.TestCase):
    def setUp(self):
        # Create test company
        self.company = frappe.get_doc({
            "doctype": "CM Company",
            "company_name": "Test Company for Employee"
        })
        self.company.insert()
        
        # Create test department
        self.department = frappe.get_doc({
            "doctype": "CM Department",
            "department_name": "Test Department for Employee",
            "company": self.company.name
        })
        self.department.insert()
    
    def test_employee_creation(self):
        employee = frappe.get_doc({
            "doctype": "CM Employee",
            "employee_name": "Test Employee",
            "email_address": "test@employee.com",
            "company": self.company.name,
            "department": self.department.name,
            "hired_on": "2024-01-01"
        })
        employee.insert()
        
        self.assertEqual(employee.employee_name, "Test Employee")
        self.assertEqual(employee.company, self.company.name)
        self.assertEqual(employee.department, self.department.name)
        
        # Clean up
        frappe.delete_doc("CM Employee", employee.name)
    
    def test_days_employed_calculation(self):
        employee = frappe.get_doc({
            "doctype": "CM Employee",
            "employee_name": "Test Employee Days",
            "email_address": "test.days@employee.com",
            "company": self.company.name,
            "department": self.department.name,
            "hired_on": "2024-01-01"
        })
        employee.insert()
        
        # Check that days_employed is calculated
        self.assertIsNotNone(employee.days_employed)
        self.assertGreater(employee.days_employed, 0)
        
        # Verify calculation
        expected_days = date_diff(getdate(), employee.hired_on)
        self.assertEqual(employee.days_employed, expected_days)
        
        # Clean up
        frappe.delete_doc("CM Employee", employee.name)
    
    def test_email_validation(self):
        with self.assertRaises(frappe.ValidationError):
            employee = frappe.get_doc({
                "doctype": "CM Employee",
                "employee_name": "Test Invalid Email",
                "email_address": "invalid-email",
                "company": self.company.name,
                "department": self.department.name
            })
            employee.insert()
    
    def test_department_count_update(self):
        # Check initial department count
        self.department.reload()
        initial_count = self.department.number_of_employees
        
        # Create employee
        employee = frappe.get_doc({
            "doctype": "CM Employee",
            "employee_name": "Test Employee Count",
            "email_address": "test.count@employee.com",
            "company": self.company.name,
            "department": self.department.name
        })
        employee.insert()
        
        # Check that department count is updated
        self.department.reload()
        self.assertEqual(self.department.number_of_employees, initial_count + 1)
        
        # Clean up
        frappe.delete_doc("CM Employee", employee.name)
    
    def tearDown(self):
        # Clean up test data
        try:
            frappe.delete_doc("CM Department", self.department.name)
            frappe.delete_doc("CM Company", self.company.name)
        except:
            pass