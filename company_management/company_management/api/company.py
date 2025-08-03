import frappe
from frappe import _
from company_management.company_management.auth.security import require_permission, filter_by_user_company

@frappe.whitelist(allow_guest=False)
@require_permission("Company", "read")
def get_companies():
    """Get all companies"""
    try:
        filters = filter_by_user_company("Company")
        companies = frappe.get_all('Company', 
                                 filters=filters,
                                 fields=['name', 'company_name', 'number_of_departments', 
                                        'number_of_employees', 'number_of_projects',
                                        'email', 'phone', 'website'])
        return {"success": True, "data": companies}
    except Exception as e:
        frappe.log_error(f"Error fetching companies: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False)
@require_permission("Company", "read")
def get_company(name):
    """Get single company"""
    try:
        company = frappe.get_doc('Company', name)
        return {"success": True, "data": company.as_dict()}
    except Exception as e:
        frappe.log_error(f"Error fetching company {name}: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['POST'])
@require_permission("Company", "create")
def create_company():
    """Create new company"""
    try:
        data = frappe.local.form_dict
        company = frappe.new_doc('Company')
        company.update(data)
        company.insert()
        return {"success": True, "data": company.as_dict()}
    except Exception as e:
        frappe.log_error(f"Error creating company: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['PATCH'])
@require_permission("Company", "write")
def update_company(name):
    """Update existing company"""
    try:
        data = frappe.local.form_dict
        company = frappe.get_doc('Company', name)
        company.update(data)
        company.save()
        return {"success": True, "data": company.as_dict()}
    except Exception as e:
        frappe.log_error(f"Error updating company {name}: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=False, methods=['DELETE'])
@require_permission("Company", "delete")
def delete_company(name):
    """Delete company"""
    try:
        frappe.delete_doc('Company', name)
        return {"success": True, "message": "Company deleted successfully"}
    except Exception as e:
        frappe.log_error(f"Error deleting company {name}: {str(e)}")
        return {"success": False, "error": str(e)}