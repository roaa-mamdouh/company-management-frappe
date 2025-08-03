import frappe

def create_custom_roles():
    roles = [
        {
            "role_name": "Company Admin",
            "desk_access": 1,
            "description": "Full access to company management system"
        },
        {
            "role_name": "Department Manager",
            "desk_access": 1,
            "description": "Manage department and employee data"
        },
        {
            "role_name": "Employee User",
            "desk_access": 1,
            "description": "Limited access to personal data"
        }
    ]
    
    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.new_doc("Role")
            role.update(role_data)
            role.insert()

def setup_permissions():
    # Company permissions
    set_doctype_permissions("Company", [
        {"role": "Company Admin", "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "Department Manager", "read": 1, "write": 0, "create": 0, "delete": 0},
        {"role": "Employee User", "read": 1, "write": 0, "create": 0, "delete": 0}
    ])
    
    # Employee permissions
    set_doctype_permissions("Employee", [
        {"role": "Company Admin", "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "Department Manager", "read": 1, "write": 1, "create": 1, "delete": 0},
        {"role": "Employee User", "read": 1, "write": 0, "create": 0, "delete": 0}
    ])
    
    # Department permissions
    set_doctype_permissions("Department", [
        {"role": "Company Admin", "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "Department Manager", "read": 1, "write": 1, "create": 0, "delete": 0},
        {"role": "Employee User", "read": 1, "write": 0, "create": 0, "delete": 0}
    ])
    
    # Project permissions
    set_doctype_permissions("Project", [
        {"role": "Company Admin", "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "Department Manager", "read": 1, "write": 1, "create": 1, "delete": 0},
        {"role": "Employee User", "read": 1, "write": 0, "create": 0, "delete": 0}
    ])
    
    # Performance Review permissions
    set_doctype_permissions("Performance Review", [
        {"role": "Company Admin", "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1},
        {"role": "Department Manager", "read": 1, "write": 1, "create": 1, "delete": 0, "submit": 1},
        {"role": "Employee User", "read": 1, "write": 0, "create": 0, "delete": 0, "submit": 0}
    ])
    
    # User Account permissions
    set_doctype_permissions("User Account", [
        {"role": "Company Admin", "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "Department Manager", "read": 1, "write": 0, "create": 0, "delete": 0},
        {"role": "Employee User", "read": 1, "write": 0, "create": 0, "delete": 0}
    ])

def set_doctype_permissions(doctype, permissions):
    for perm in permissions:
        if not frappe.db.exists("Custom DocPerm", {
            "parent": doctype,
            "role": perm["role"]
        }):
            doc_perm = frappe.new_doc("Custom DocPerm")
            doc_perm.parent = doctype
            doc_perm.parenttype = "DocType"
            doc_perm.parentfield = "permissions"
            doc_perm.update(perm)
            doc_perm.insert()

def setup_role_profiles():
    """Create role profiles for easier user management"""
    role_profiles = [
        {
            "role_profile": "Company Administrator",
            "roles": ["Company Admin", "System Manager"]
        },
        {
            "role_profile": "Department Manager Profile", 
            "roles": ["Department Manager", "Employee User"]
        },
        {
            "role_profile": "Employee Profile",
            "roles": ["Employee User"]
        }
    ]
    
    for profile_data in role_profiles:
        if not frappe.db.exists("Role Profile", profile_data["role_profile"]):
            role_profile = frappe.new_doc("Role Profile")
            role_profile.role_profile = profile_data["role_profile"]
            
            for role in profile_data["roles"]:
                role_profile.append("roles", {"role": role})
            
            role_profile.insert()