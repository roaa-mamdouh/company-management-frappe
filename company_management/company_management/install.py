import frappe
from company_management.company_management.setup.roles import create_custom_roles, setup_permissions, setup_role_profiles
from company_management.company_management.workflow.performance_review_workflow import create_employee_performance_review_workflow, setup_workflow_notifications

def after_install():
    """Setup after app installation"""
    print("Setting up Company Management System...")
    
    try:
        # Create custom roles
        print("Creating custom roles...")
        create_custom_roles()
        
        # Setup permissions
        print("Setting up permissions...")
        setup_permissions()
        
        # Setup role profiles
        print("Setting up role profiles...")
        setup_role_profiles()
        
        # Create Employee Performance Review Cycle workflow
        print("Creating Employee Performance Review Cycle workflow...")
        try:
            create_employee_performance_review_workflow()
        except Exception as workflow_error:
            print(f"Warning: Could not create workflow: {str(workflow_error)}")
        
        # Create default data
        print("Creating default data...")
        try:
            setup_default_data()
        except Exception as data_error:
            print(f"Warning: Could not create default data: {str(data_error)}")
        
        # Setup email templates
        print("Setting up email templates...")
        try:
            setup_default_email_templates()
        except Exception as template_error:
            print(f"Warning: Could not create email templates: {str(template_error)}")
        
        # Create sample projects
        print("Creating sample projects...")
        try:
            create_sample_projects()
        except Exception as project_error:
            print(f"Warning: Could not create sample projects: {str(project_error)}")
        
        # Setup database indexes for performance
        print("Setting up database indexes...")
        try:
            setup_database_indexes()
        except Exception as index_error:
            print(f"Warning: Could not create database indexes: {str(index_error)}")
        
        print("Company Management System setup completed!")
        
    except Exception as e:
        print(f"Error during installation: {str(e)}")
        # Don't log the error to avoid the database field length issue

def setup_default_data():
    """Create default companies and departments for testing"""
    try:
        # Create demo company
        if not frappe.db.exists("Company", "Demo Company"):
            company = frappe.new_doc("Company")
            company.company_name = "Demo Company"
            company.description = "Demo company for testing purposes"
            company.email = "info@democompany.com"
            company.phone = "+1-555-0123"
            company.website = "https://democompany.com"
            company.address = "123 Demo Street"
            company.city = "Demo City"
            company.state = "Demo State"
            company.country = "Demo Country"
            company.postal_code = "12345"
            company.established_date = "2020-01-01"
            company.insert()
            print(f"Created demo company: {company.name}")
            
            # Create demo departments
            departments = [
                {
                    "department_name": "IT Department",
                    "description": "Information Technology Department",
                    "company": company.name
                },
                {
                    "department_name": "HR Department", 
                    "description": "Human Resources Department",
                    "company": company.name
                },
                {
                    "department_name": "Finance Department",
                    "description": "Finance and Accounting Department", 
                    "company": company.name
                }
            ]
            
            for dept_data in departments:
                if not frappe.db.exists("Department", dept_data["department_name"]):
                    dept = frappe.new_doc("Department")
                    dept.update(dept_data)
                    dept.insert()
                    print(f"Created demo department: {dept.name}")
            
            # Create demo employees - skip due to potential conflicts with existing Employee DocType
            print("Skipping demo employee creation to avoid conflicts with existing Employee DocType")
                        
            frappe.db.commit()
            
    except Exception as e:
        frappe.log_error(f"Error creating default data: {str(e)}")
        print(f"Error creating default data: {str(e)}")

def create_sample_projects():
    """Create sample projects for demo"""
    try:
        if frappe.db.exists("Company", "Demo Company"):
            projects = [
                {
                    "project_name": "Website Redesign",
                    "company": "Demo Company",
                    "department": "IT Department",
                    "description": "Complete redesign of company website",
                    "start_date": "2025-01-01",
                    "end_date": "2025-03-31",
                    "status": "In Progress",
                    "budget": 50000,
                    "priority": "High"
                },
                {
                    "project_name": "HR System Implementation",
                    "company": "Demo Company", 
                    "department": "HR Department",
                    "description": "Implementation of new HR management system",
                    "start_date": "2025-02-01",
                    "end_date": "2025-06-30",
                    "status": "Planning",
                    "budget": 75000,
                    "priority": "Medium"
                }
            ]
            
            for proj_data in projects:
                if not frappe.db.exists("Project", proj_data["project_name"]):
                    project = frappe.new_doc("Project")
                    project.update(proj_data)
                    project.insert()
                    print(f"Created demo project: {project.name}")
                    
            frappe.db.commit()
            
    except Exception as e:
        frappe.log_error(f"Error creating sample projects: {str(e)}")
        print(f"Error creating sample projects: {str(e)}")

def setup_default_email_templates():
    """Setup email templates for notifications"""
    try:
        templates = [
            {
                "name": "Performance Review Scheduled",
                "subject": "Performance Review Scheduled - {{ doc.employee }}",
                "response": """
                <p>Dear {{ frappe.get_value('Employee', doc.employee, 'employee_name') }},</p>
                
                <p>Your performance review has been scheduled for the period {{ doc.review_period_start }} to {{ doc.review_period_end }}.</p>
                
                <p>Reviewer: {{ frappe.get_value('Employee', doc.reviewer, 'employee_name') }}</p>
                <p>Review Date: {{ doc.review_date or 'To be confirmed' }}</p>
                
                <p>Please prepare for your review by gathering relevant work samples and achievements from this period.</p>
                
                <p>Best regards,<br>HR Team</p>
                """
            },
            {
                "name": "Performance Review Approved",
                "subject": "Performance Review Approved - {{ doc.employee }}", 
                "response": """
                <p>Dear {{ frappe.get_value('Employee', doc.employee, 'employee_name') }},</p>
                
                <p>Your performance review for the period {{ doc.review_period_start }} to {{ doc.review_period_end }} has been approved.</p>
                
                <p>Overall Rating: {{ doc.overall_rating }}</p>
                
                {% if doc.development_plan %}
                <p>Development Plan: {{ doc.development_plan }}</p>
                {% endif %}
                
                <p>Congratulations on your performance!</p>
                
                <p>Best regards,<br>Management Team</p>
                """
            }
        ]
        
        for template_data in templates:
            if not frappe.db.exists("Email Template", template_data["name"]):
                template = frappe.new_doc("Email Template")
                template.update(template_data)
                template.insert()
                print(f"Created email template: {template.name}")
                
        frappe.db.commit()
        
    except Exception as e:
        frappe.log_error(f"Error creating email templates: {str(e)}")
        print(f"Error creating email templates: {str(e)}")

def setup_database_indexes():
    """Add database indexes for better performance"""
    try:
        print("Adding database indexes for improved performance...")
        
        # Employee indexes
        frappe.db.add_index("Employee", ["company", "department"])
        frappe.db.add_index("Employee", ["email_address"])
        frappe.db.add_index("Employee", ["status"])
        
        # Project indexes  
        frappe.db.add_index("Project", ["company", "department"])
        frappe.db.add_index("Project", ["start_date", "end_date"])
        frappe.db.add_index("Project", ["status"])
        
        # Performance Review indexes
        frappe.db.add_index("Performance Review", ["employee", "workflow_state"])
        frappe.db.add_index("Performance Review", ["reviewer"])
        frappe.db.add_index("Performance Review", ["review_period_start", "review_period_end"])
        
        # Department indexes
        frappe.db.add_index("Department", ["company"])
        
        frappe.db.commit()
        print("Database indexes created successfully")
        
    except Exception as e:
        print(f"Error creating database indexes: {str(e)}")

def create_default_user_account():
    """Create default admin user account"""
    try:
        if not frappe.db.exists("User Account", "admin@company.com"):
            user_account = frappe.new_doc("User Account")
            user_account.full_name = "System Administrator"
            user_account.email_address = "admin@company.com"
            user_account.user_type = "Admin"
            user_account.role = "Company Admin"
            user_account.company = "Demo Company"
            user_account.is_active = 1
            user_account.insert()
            print(f"Created default admin user account: {user_account.name}")
            
    except Exception as e:
        print(f"Error creating default user account: {str(e)}")