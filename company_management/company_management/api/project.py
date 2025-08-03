import frappe
from frappe import _
from company_management.company_management.auth.security import require_permission, filter_by_user_company

@frappe.whitelist(allow_guest=False, methods=['POST'])
@require_permission("Project", "create")
def create_project():
    """Create new project"""
    try:
        data = frappe.local.form_dict
        project = frappe.new_doc('Project')
        project.update(data)
        project.insert()
        return {"success": True, "data": project.as_dict()}
    except Exception as e:
        frappe.log_error(f"Error creating project: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['GET'])
@require_permission("Project", "read")
def get_projects():
    """Get all projects"""
    try:
        filters = filter_by_user_company("Project")
        projects = frappe.get_all('Project',
                                filters=filters,
                                fields=['name', 'project_name', 'company', 'department',
                                       'project_manager', 'start_date', 'end_date', 'status',
                                       'budget', 'priority'])
        return {"success": True, "data": projects}
    except Exception as e:
        frappe.log_error(f"Error fetching projects: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['GET'])
@require_permission("Project", "read")
def get_project(name):
    """Get single project"""
    try:
        project = frappe.get_doc('Project', name)
        return {"success": True, "data": project.as_dict()}
    except Exception as e:
        frappe.log_error(f"Error fetching project {name}: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['PATCH'])
@require_permission("Project", "write")
def update_project(name):
    """Update existing project"""
    try:
        data = frappe.local.form_dict
        project = frappe.get_doc('Project', name)
        project.update(data)
        project.save()
        return {"success": True, "data": project.as_dict()}
    except Exception as e:
        frappe.log_error(f"Error updating project {name}: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['DELETE'])
@require_permission("Project", "delete")
def delete_project(name):
    """Delete project"""
    try:
        frappe.delete_doc('Project', name)
        return {"success": True, "message": "Project deleted successfully"}
    except Exception as e:
        frappe.log_error(f"Error deleting project {name}: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['GET'])
@require_permission("Project", "read")
def get_projects_by_department(department):
    """Get projects by department"""
    try:
        filters = filter_by_user_company("Project", {"department": department})
        projects = frappe.get_all('Project',
                                filters=filters,
                                fields=['name', 'project_name', 'project_manager',
                                       'start_date', 'end_date', 'status', 'priority'])
        return {"success": True, "data": projects}
    except Exception as e:
        frappe.log_error(f"Error fetching projects for department {department}: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['GET'])
@require_permission("Project", "read")
def get_project_team(name):
    """Get project team members"""
    try:
        project = frappe.get_doc('Project', name)
        team_members = []
        
        if project.assigned_employees:
            for emp in project.assigned_employees:
                employee_data = frappe.get_value('Employee', emp.employee,
                                               ['employee_name', 'email_address', 'designation'],
                                               as_dict=True)
                if employee_data:
                    team_members.append({
                        "employee": emp.employee,
                        "employee_name": employee_data.employee_name,
                        "email_address": employee_data.email_address,
                        "designation": employee_data.designation,
                        "role": emp.role,
                        "allocated_hours": emp.allocated_hours,
                        "hourly_rate": emp.hourly_rate
                    })
        
        return {"success": True, "data": team_members}
    except Exception as e:
        frappe.log_error(f"Error fetching team for project {name}: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['POST'])
@require_permission("Project", "write")
def assign_employee_to_project(project_name, employee, role=None, allocated_hours=None, hourly_rate=None):
    """Assign employee to project"""
    try:
        project = frappe.get_doc('Project', project_name)
        
        # Check if employee already assigned
        existing = [emp for emp in project.assigned_employees if emp.employee == employee]
        if existing:
            return {"success": False, "error": "Employee already assigned to this project"}
        
        project.append('assigned_employees', {
            'employee': employee,
            'role': role,
            'allocated_hours': allocated_hours,
            'hourly_rate': hourly_rate
        })
        
        project.save()
        return {"success": True, "data": project.as_dict()}
    except Exception as e:
        frappe.log_error(f"Error assigning employee to project: {str(e)}")
        return {"success": False, "error": str(e)}