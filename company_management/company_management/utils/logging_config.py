import logging
import frappe
import os

def setup_logging():
    """Configure application logging"""
    logger = logging.getLogger('company_management')
    
    # Avoid adding multiple handlers
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(logging.INFO)
    
    # Create logs directory if it doesn't exist
    log_dir = frappe.get_site_path('logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # File handler
    log_file = os.path.join(log_dir, 'company_management.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Usage in modules
logger = setup_logging()

def log_api_access(endpoint, user, method="GET", success=True, error_msg=None):
    """Log API access attempts"""
    if success:
        logger.info(f"API Access: {method} {endpoint} by {user} - SUCCESS")
    else:
        logger.warning(f"API Access: {method} {endpoint} by {user} - FAILED: {error_msg}")

def log_workflow_action(doctype, docname, action, user, success=True, error_msg=None):
    """Log workflow actions"""
    if success:
        logger.info(f"Workflow Action: {action} on {doctype} {docname} by {user} - SUCCESS")
    else:
        logger.error(f"Workflow Action: {action} on {doctype} {docname} by {user} - FAILED: {error_msg}")

def log_user_activity(user, activity, details=None):
    """Log user activities"""
    details_str = f" - {details}" if details else ""
    logger.info(f"User Activity: {user} - {activity}{details_str}")

def log_system_event(event, details=None):
    """Log system events"""
    details_str = f" - {details}" if details else ""
    logger.info(f"System Event: {event}{details_str}")

def log_performance_metric(operation, duration, details=None):
    """Log performance metrics"""
    details_str = f" - {details}" if details else ""
    logger.info(f"Performance: {operation} took {duration:.2f}ms{details_str}")

def log_security_event(event, user, ip_address=None, details=None):
    """Log security events"""
    ip_str = f" from {ip_address}" if ip_address else ""
    details_str = f" - {details}" if details else ""
    logger.warning(f"Security Event: {event} by {user}{ip_str}{details_str}")