import frappe
import unittest
import json
from company_management.company_management.api import company, employee, department, project

class TestAPI(unittest.TestCase):
    def setUp(self):
        # Set up test user with proper permissions
        if not frappe.db.exists("User", "test@api.com"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "test@api.com",
                "first_name": "Test",
                "last_name": "API",
                "send_welcome_email": 0
            })
            user.insert()
            
            # Add System Manager role for testing
            user.add_roles("System Manager")
        
        frappe.set_user("test@api.com")
        
        # Create test company
        self.test_company = frappe.get_doc({
            "doctype": "CM Company",
            "company_name": "API Test Company"
        })
        self.test_company.insert()
    
    def test_company_api_get_companies(self):
        # Test GET companies endpoint
        response = company.get_companies()
        self.assertIsInstance(response, dict)
        self.assertTrue(response.get("success"))
        self.assertIn("data", response)
        self.assertIsInstance(response["data"], list)
    
    def test_company_api_get_company(self):
        # Test GET single company
        response = company.get_company(self.test_company.name)
        self.assertTrue(response.get("success"))
        self.assertEqual(response["data"]["company_name"], "API Test Company")
    
    def test_employee_crud_api(self):
        # Create test department first
        dept = frappe.get_doc({
            "doctype": "CM Department",
            "department_name": "API Test Department",
            "company": self.test_company.name
        })
        dept.insert()
        
        # Test POST employee
        frappe.local.form_dict = {
            "employee_name": "API Test Employee",
            "email_address": "api.test@employee.com",
            "company": self.test_company.name,
            "department": dept.name
        }
        
        # Create
        response = employee.create_employee()
        self.assertTrue(response.get("success"))
        employee_name = response.get("data", {}).get("name")
        self.assertIsNotNone(employee_name)
        
        # Read
        get_response = employee.get_employee(employee_name)
        self.assertTrue(get_response.get("success"))
        self.assertEqual(get_response["data"]["employee_name"], "API Test Employee")
        
        # Update
        frappe.local.form_dict = {"designation": "Senior Developer"}
        update_response = employee.update_employee(employee_name)
        self.assertTrue(update_response.get("success"))
        self.assertEqual(update_response["data"]["designation"], "Senior Developer")
        
        # Delete
        delete_response = employee.delete_employee(employee_name)
        self.assertTrue(delete_response.get("success"))
        
        # Verify deletion
        self.assertFalse(frappe.db.exists("CM Employee", employee_name))
        
        # Clean up department
        frappe.delete_doc("CM Department", dept.name)
    
    def test_department_api(self):
        # Test GET departments
        response = department.get_departments()
        self.assertTrue(response.get("success"))
        self.assertIsInstance(response["data"], list)
        
        # Test POST department
        frappe.local.form_dict = {
            "department_name": "API Test Dept",
            "company": self.test_company.name,
            "description": "Department created via API"
        }
        
        create_response = department.create_department()
        self.assertTrue(create_response.get("success"))
        dept_name = create_response["data"]["name"]
        
        # Test GET single department
        get_response = department.get_department(dept_name)
        self.assertTrue(get_response.get("success"))
        self.assertEqual(get_response["data"]["department_name"], "API Test Dept")
        
        # Clean up
        frappe.delete_doc("CM Department", dept_name)
    
    def test_project_api(self):
        # Create test department
        dept = frappe.get_doc({
            "doctype": "CM Department",
            "department_name": "Project API Test Dept",
            "company": self.test_company.name
        })
        dept.insert()
        
        # Test POST project
        frappe.local.form_dict = {
            "project_name": "API Test Project",
            "company": self.test_company.name,
            "department": dept.name,
            "start_date": "2025-01-01",
            "status": "Planning"
        }
        
        create_response = project.create_project()
        self.assertTrue(create_response.get("success"))
        project_name = create_response["data"]["name"]
        
        # Test GET projects
        get_response = project.get_projects()
        self.assertTrue(get_response.get("success"))
        
        # Test GET single project
        single_response = project.get_project(project_name)
        self.assertTrue(single_response.get("success"))
        self.assertEqual(single_response["data"]["project_name"], "API Test Project")
        
        # Clean up
        frappe.delete_doc("CM Project", project_name)
        frappe.delete_doc("CM Department", dept.name)
    
    def test_api_error_handling(self):
        # Test accessing non-existent company
        response = company.get_company("NonExistentCompany")
        self.assertFalse(response.get("success"))
        self.assertIn("error", response)
        
        # Test creating employee without required fields
        frappe.local.form_dict = {
            "employee_name": "Incomplete Employee"
            # Missing required fields like email_address, company
        }
        
        response = employee.create_employee()
        self.assertFalse(response.get("success"))
        self.assertIn("error", response)
    
    def tearDown(self):
        # Clean up test data
        try:
            frappe.delete_doc("CM Company", self.test_company.name)
            frappe.delete_doc("User", "test@api.com")
        except:
            pass
        
        # Reset user
        frappe.set_user("Administrator")