import frappe
from frappe import _
from company_management.company_management.auth.security import require_permission, filter_by_user_company

@frappe.whitelist(allow_guest=False, methods=['GET'])
@require_permission("Department", "read")
def get_departments():
    """Get all departments"""
    try:
        filters = filter_by_user_company("Department")
        departments = frappe.get_all('Department',
                                   filters=filters,
                                   fields=['name', 'department_name', 'company', 'manager',
                                          'number_of_employees', 'number_of_projects', 'created_date'])
        return {"success": True, "data": departments}
    except Exception as e:
        frappe.log_error(f"Error fetching departments: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['GET'])
@require_permission("Department", "read")
def get_department(name):
    """Get single department"""
    try:
        department = frappe.get_doc('Department', name)
        return {"success": True, "data": department.as_dict()}
    except Exception as e:
        frappe.log_error(f"Error fetching department {name}: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['POST'])
@require_permission("Department", "create")
def create_department():
    """Create new department"""
    try:
        data = frappe.local.form_dict
        department = frappe.new_doc('Department')
        department.update(data)
        department.insert()
        return {"success": True, "data": department.as_dict()}
    except Exception as e:
        frappe.log_error(f"Error creating department: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['PATCH'])
@require_permission("Department", "write")
def update_department(name):
    """Update existing department"""
    try:
        data = frappe.local.form_dict
        department = frappe.get_doc('Department', name)
        department.update(data)
        department.save()
        return {"success": True, "data": department.as_dict()}
    except Exception as e:
        frappe.log_error(f"Error updating department {name}: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['DELETE'])
@require_permission("Department", "delete")
def delete_department(name):
    """Delete department"""
    try:
        frappe.delete_doc('Department', name)
        return {"success": True, "message": "Department deleted successfully"}
    except Exception as e:
        frappe.log_error(f"Error deleting department {name}: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['GET'])
@require_permission("Department", "read")
def get_departments_by_company(company):
    """Get departments by company"""
    try:
        departments = frappe.get_all('Department',
                                   filters={'company': company},
                                   fields=['name', 'department_name', 'manager',
                                          'number_of_employees', 'number_of_projects'])
        return {"success": True, "data": departments}
    except Exception as e:
        frappe.log_error(f"Error fetching departments for company {company}: {str(e)}")
        return {"success": False, "error": str(e)}