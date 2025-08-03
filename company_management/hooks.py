app_name = "company_management"
app_title = "Company Management"
app_publisher = "Roaa"
app_description = "A comprehensive Company Management System built with Frappe Framework featuring CRUD operations, workflow management for employee performance reviews, and role-based access control."
app_email = "roaaabdelhadyy@gmail.com"
app_license = "unlicense"

# Apps
# ------------------

# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/company_management/css/company_management.css"
# app_include_js = "/assets/company_management/js/company_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/company_management/css/company_management.css"
# web_include_js = "/assets/company_management/js/company_management.js"

# Installation
# ------------

# before_install = "company_management.install.before_install"
after_install = "company_management.company_management.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "company_management.uninstall.before_uninstall"
# after_uninstall = "company_management.uninstall.after_uninstall"

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Company": {
		"validate": "company_management.company_management.auth.security.validate_company_access"
	},
	"Department": {
		"validate": "company_management.company_management.auth.security.validate_company_access"
	},
	"Employee": {
		"validate": "company_management.company_management.auth.security.validate_company_access"
	},
	"Project": {
		"validate": "company_management.company_management.auth.security.validate_company_access"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"company_management.tasks.all"
# 	],
# 	"daily": [
# 		"company_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"company_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"company_management.tasks.weekly"
# 	],
# 	"monthly": [
# 		"company_management.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "company_management.install.before_tests"

