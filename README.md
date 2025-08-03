# Company Management System

A comprehensive Company Management System built with Frappe Framework featuring CRUD operations, workflow management for employee performance reviews, and role-based access control.

## Features

### 🏢 Core Business Entities
- **CM Company**: Manage multiple companies with automatic statistics calculation
- **CM Department**: Organize departments within companies with auto-count features
- **CM Employee**: Complete employee management with hire date and days employed tracking  
- **CM Project**: Project management with team assignments and company validation
- **Performance Review**: Comprehensive performance review workflow with automated transitions
- **User Account**: Extended user management with role-based company access

### 🔐 Security & Access Control
- **Role-Based Access Control**: Three-tier role system (Company Admin, Department Manager, Employee User)
- **Custom Permissions**: Granular permissions for each DocType
- **Company-Level Data Isolation**: Users can only access data from their assigned company
- **User Accounts**: Extended user management with role automation

### 🔄 Workflow Management
- **Performance Review Workflow**: Multi-state workflow with automated transitions
- **Smart State Transitions**: Automatic progression based on field changes (scheduling, feedback, submission)
- **Manual Approval Process**: Manager-controlled approval and rejection workflow actions
- **Email Notifications**: Automatic notifications for workflow state changes

### 🌐 REST API
- **Complete CRUD Operations**: Full REST API for all entities
- **Security Integration**: API endpoints respect role-based permissions
- **Error Handling**: Comprehensive error handling and logging
- **Response Standardization**: Consistent JSON response format

## Installation

### Prerequisites
- Frappe Framework 15.x or higher
- Python 3.8+
- Node.js 18+

### Quick Installation

```bash
# Clone the repository
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/roaa-mamdouh/company-management-frappe.git
bench install-app company_management

# Or install from a specific site
bench --site your-site install-app company_management
```

### Development Installation

```bash
# Get the app
bench get-app https://github.com/roaa-mamdouh/company-management-frappe.git --branch main

# Install on your site
bench --site your-site install-app company_management

# Migrate to create database tables
bench --site your-site migrate

# Start development server
bench start
```

## API Documentation

The system provides a comprehensive REST API for all operations. All endpoints require authentication and respect role-based permissions.

### Base URL
```
/api/method/company_management.api.{module}.{function}
```

### Companies API

#### Get All Companies
```http
GET /api/method/company_management.api.company.get_companies
```

#### Get Single Company
```http
GET /api/method/company_management.api.company.get_company?name={company_name}
```

#### Create Company
```http
POST /api/method/company_management.api.company.create_company
Content-Type: application/json

{
  "company_name": "New Company",
  "email": "info@newcompany.com",
  "phone": "+1-555-0123"
}
```

### Employees API

#### Get All Employees
```http
GET /api/method/company_management.api.employee.get_employees
```

#### Create Employee
```http
POST /api/method/company_management.api.employee.create_employee
Content-Type: application/json

{
  "employee_name": "John Doe",
  "email_address": "john.doe@company.com",
  "company": "Demo Company",
  "department": "IT Department",
  "designation": "Software Developer"
}
```

#### Update Employee
```http
PATCH /api/method/company_management.api.employee.update_employee?name={employee_name}
Content-Type: application/json

{
  "designation": "Senior Software Developer",
  "salary": 75000
}
```

### Performance Reviews API

#### Get Pending Reviews
```http
GET /api/method/company_management.api.performance_review.get_pending_reviews
```

#### Execute Workflow Action
```http
POST /api/method/company_management.api.performance_review.workflow_action
Content-Type: application/json

{
  "name": "PR-2025-00001",
  "action": "Approve"
}
```

### Response Format

All API endpoints return responses in the following format:

```json
{
  "success": true,
  "data": {
    // Response data here
  }
}
```

For errors:
```json
{
  "success": false,
  "error": "Error message description"
}
```

## User Roles

### Company Admin
- Full access to all company data
- Can create, read, update, and delete all entities
- Can approve performance reviews
- Can manage user accounts

### Department Manager  
- Access to their company's data
- Can manage employees and projects in their department
- Can create and update performance reviews
- Cannot delete companies or manage user accounts

### Employee User
- Read-only access to company data
- Can view their own performance reviews
- Cannot create, update, or delete any entities

## Workflow States

### Performance Review Workflow

The system features both **automated** and **manual** transitions:

#### Automated Transitions (based on field changes):
1. **Pending Review** → **Review Scheduled**: When `review_date` is set
2. **Review Scheduled** → **Feedback Provided**: When `feedback` is provided
3. **Feedback Provided** → **Under Approval**: When `submitted_for_approval` is checked
4. **Review Rejected** → **Feedback Provided**: When feedback is updated after rejection

#### Manual Transitions (workflow actions):
- **Under Approval** → **Review Approved**: Manager/Admin approves
- **Under Approval** → **Review Rejected**: Manager/Admin rejects

This hybrid approach ensures smooth workflow progression while maintaining control over critical approval decisions.

## Key Features

### Automated Field Calculations
- **Employee Days Employed**: Automatically calculated from hire date
- **Company Statistics**: Auto-updated counts of departments, employees, and projects with caching
- **Department Counts**: Auto-calculated employee and project counts per department

### Data Validation & Relationships
- **Email Validation**: Ensures valid email formats for employees and user accounts
- **Date Validation**: Prevents invalid date ranges in projects (end date before start date)
- **Company Consistency**: Validates that project employees belong to the same company
- **Relationship Integrity**: Maintains proper links between companies, departments, and employees

### Security Features
- **Role-Based Data Filtering**: Users only see data from their assigned company
- **Permission Decorators**: API endpoints automatically enforce role permissions
- **Workflow Action Security**: Role-based validation for workflow transitions
- **Company-Level Isolation**: Complete data separation between companies

### Performance & Monitoring
- **Smart Caching**: Cached company statistics and employee performance data
- **Comprehensive Logging**: Detailed logging for API access, workflow actions, and security events
- **Performance Metrics**: Built-in performance tracking and monitoring

## Testing

Run the test suite with:

```bash
# Run all tests
bench --site your-site run-tests company_management

# Run specific test module
bench --site your-site run-tests company_management.tests.test_company

# Run with verbose output
bench --site your-site run-tests company_management --verbose
```

## Development

### Project Structure

```
company_management/
├── company_management/
│   ├── api/                    # REST API endpoints
│   ├── auth/                   # Authentication & security  
│   ├── doctype/               # DocType definitions
│   ├── fixtures/              # Workflow and setup data
│   ├── setup/                 # Installation scripts & roles
│   ├── tests/                 # Unit tests
│   ├── utils/                 # Caching & logging utilities
│   ├── workflow/              # Workflow definitions
│   ├── hooks.py               # Frappe hooks
│   └── install.py             # Installation logic
├── README.md
├── license.txt
└── pyproject.toml
```

### DocTypes

- **CM Company**: Main company entity with auto-calculated department, employee, and project counts
- **CM Department**: Department management with automatic employee/project counting and company linking
- **CM Employee**: Employee records with automatic days employed calculation and department/company relationships
- **CM Project**: Project management with team assignments and employee-company validation
- **Performance Review**: Submittable document with automated workflow transitions
- **User Account**: Extended user management with role-based company access
- **CM Project Employee**: Child table for project team assignments with role and hourly rate tracking

> **Note**: DocTypes are prefixed with "CM" to avoid conflicts with Frappe's built-in Employee, Company, Department, and Project DocTypes.

### Code Quality

This project maintains high code quality standards using:

- **Ruff**: Fast Python linter and formatter (configured in pyproject.toml)
- **Type hints**: Python 3.10+ typing for better code clarity
- **Comprehensive testing**: Unit tests for all API endpoints and workflows
- **Security**: Role-based access control and input validation

### Development Guidelines

1. **Follow Frappe conventions** for naming and file structure
2. **Write tests** for all new features and bug fixes
3. **Use proper error handling** in all API endpoints
4. **Document API changes** in this README
5. **Respect role-based permissions** in all operations

## Troubleshooting

### Common Issues

**Installation fails**: Ensure you have the correct Frappe version and all dependencies installed.

**Permission errors**: Check that users have the correct roles assigned and that role permissions are properly set up.

**API not working**: Verify that the user is authenticated and has the required permissions for the operation.

**Workflow not progressing**: Check that the user has the correct role for the workflow transition.

### Support

For issues and questions:
1. Check the [GitHub Issues](https://github.com/roaa-mamdouh/company-management-frappe/issues)
2. Create a new issue with detailed information
3. Include error logs and steps to reproduce

## License

unlicense

## Credits

Built with ❤️ using [Frappe Framework](https://frappeframework.com/)

🤖 Generated with [Claude Code](https://claude.ai/code)
