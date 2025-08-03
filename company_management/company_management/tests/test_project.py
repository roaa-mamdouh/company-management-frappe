import frappe
import unittest
from frappe.utils import getdate

class TestProject(unittest.TestCase):
    def setUp(self):
        # Create test company
        self.company = frappe.get_doc({
            "doctype": "CM Company",
            "company_name": "Test Company for Project"
        })
        self.company.insert()
        
        # Create test department
        self.department = frappe.get_doc({
            "doctype": "CM Department", 
            "department_name": "Test Department for Project",
            "company": self.company.name
        })
        self.department.insert()
        
        # Create test employee
        self.employee = frappe.get_doc({
            "doctype": "CM Employee",
            "employee_name": "Test Project Manager",
            "email_address": "test.pm@project.com",
            "company": self.company.name,
            "department": self.department.name
        })
        self.employee.insert()
    
    def test_project_creation(self):
        project = frappe.get_doc({
            "doctype": "CM Project",
            "project_name": "Test Project",
            "company": self.company.name,
            "department": self.department.name,
            "project_manager": self.employee.name,
            "start_date": "2025-01-01",
            "end_date": "2025-06-30",
            "status": "Planning"
        })
        project.insert()
        
        self.assertEqual(project.project_name, "Test Project")
        self.assertEqual(project.company, self.company.name)
        self.assertEqual(project.status, "Planning")
        
        # Clean up
        frappe.delete_doc("CM Project", project.name)
    
    def test_date_validation(self):
        # Test invalid date range (end date before start date)
        with self.assertRaises(frappe.ValidationError):
            project = frappe.get_doc({
                "doctype": "CM Project",
                "project_name": "Invalid Date Project",
                "company": self.company.name,
                "start_date": "2025-06-30",
                "end_date": "2025-01-01"
            })
            project.insert()
    
    def test_employee_assignment(self):
        # Create another employee for assignment
        emp2 = frappe.get_doc({
            "doctype": "CM Employee",
            "employee_name": "Test Developer",
            "email_address": "test.dev@project.com",
            "company": self.company.name,
            "department": self.department.name
        })
        emp2.insert()
        
        project = frappe.get_doc({
            "doctype": "CM Project",
            "project_name": "Test Assignment Project",
            "company": self.company.name,
            "department": self.department.name,
            "start_date": "2025-01-01"
        })
        
        # Add assigned employees
        project.append('assigned_employees', {
            'employee': self.employee.name,
            'role': 'Project Manager',
            'allocated_hours': 40,
            'hourly_rate': 100
        })
        
        project.append('assigned_employees', {
            'employee': emp2.name,
            'role': 'Developer',
            'allocated_hours': 35,
            'hourly_rate': 75
        })
        
        project.insert()
        
        self.assertEqual(len(project.assigned_employees), 2)
        self.assertEqual(project.assigned_employees[0].employee, self.employee.name)
        self.assertEqual(project.assigned_employees[1].employee, emp2.name)
        
        # Clean up
        frappe.delete_doc("CM Project", project.name)
        frappe.delete_doc("CM Employee", emp2.name)
    
    def test_employee_company_validation(self):
        # Create employee from different company
        other_company = frappe.get_doc({
            "doctype": "CM Company",
            "company_name": "Other Test Company"
        })
        other_company.insert()
        
        other_dept = frappe.get_doc({
            "doctype": "CM Department",
            "department_name": "Other Dept",
            "company": other_company.name
        })
        other_dept.insert()
        
        other_employee = frappe.get_doc({
            "doctype": "CM Employee",
            "employee_name": "Other Company Employee",
            "email_address": "other@company.com",
            "company": other_company.name,
            "department": other_dept.name
        })
        other_employee.insert()
        
        # Try to assign employee from different company to project
        with self.assertRaises(frappe.ValidationError):
            project = frappe.get_doc({
                "doctype": "CM Project",
                "project_name": "Cross Company Project",
                "company": self.company.name,
                "start_date": "2025-01-01"
            })
            
            project.append('assigned_employees', {
                'employee': other_employee.name,
                'role': 'Developer'
            })
            
            project.insert()
        
        # Clean up
        frappe.delete_doc("CM Employee", other_employee.name)
        frappe.delete_doc("CM Department", other_dept.name)
        frappe.delete_doc("CM Company", other_company.name)
    
    def tearDown(self):
        # Clean up test data
        try:
            frappe.delete_doc("CM Employee", self.employee.name)
            frappe.delete_doc("CM Department", self.department.name)
            frappe.delete_doc("CM Company", self.company.name)
        except:
            pass