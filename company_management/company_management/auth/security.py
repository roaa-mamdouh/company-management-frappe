import frappe
from frappe.auth import LoginManager

def check_role_permission(role, doctype, operation):
    """Check if role has permission for operation on doctype"""
    permissions = frappe.get_all("Custom DocPerm", 
                               filters={"parent": doctype, "role": role},
                               fields=[operation])
    return bool(permissions and permissions[0].get(operation))

def validate_api_access(doctype, operation):
    """Validate API access based on user role"""
    user_roles = frappe.get_roles(frappe.session.user)
    
    for role in user_roles:
        if check_role_permission(role, doctype, operation):
            return True
    
    frappe.throw("Insufficient permissions", frappe.PermissionError)

# Decorator for API endpoints
def require_permission(doctype, operation):
    def decorator(func):
        def wrapper(*args, **kwargs):
            validate_api_access(doctype, operation)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def get_user_company():
    """Get company associated with current user"""
    user_account = frappe.get_value("User Account", 
                                   {"email_address": frappe.session.user}, 
                                   "company")
    return user_account

def can_access_company_data(company):
    """Check if user can access data for specific company"""
    if "Company Admin" in frappe.get_roles():
        return True
    
    user_company = get_user_company()
    return user_company == company

def filter_by_user_company(doctype, filters=None):
    """Add company filter based on user permissions"""
    if filters is None:
        filters = {}
    
    if "Company Admin" not in frappe.get_roles():
        user_company = get_user_company()
        if user_company:
            filters["company"] = user_company
    
    return filters

def validate_company_access(doc, method):
    """Validate that user can only access their company's data"""
    if hasattr(doc, 'company') and doc.company:
        if not can_access_company_data(doc.company):
            frappe.throw("You can only access data for your company")

def setup_user_permissions():
    """Setup user permissions based on role and company"""
    user_accounts = frappe.get_all("User Account", 
                                  fields=["name", "email_address", "company", "role"])
    
    for user_account in user_accounts:
        if user_account.company and user_account.role != "Company Admin":
            # Create user permission for company
            if not frappe.db.exists("User Permission", {
                "user": user_account.email_address,
                "allow": "Company",
                "for_value": user_account.company
            }):
                user_perm = frappe.new_doc("User Permission")
                user_perm.user = user_account.email_address
                user_perm.allow = "Company"
                user_perm.for_value = user_account.company
                user_perm.insert()