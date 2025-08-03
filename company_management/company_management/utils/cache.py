import frappe
from company_management.company_management.utils.logging_config import logger

def get_cached_company_stats(company_name):
    """Get cached company statistics"""
    cache_key = f"company_stats_{company_name}"
    cached_data = frappe.cache().get_value(cache_key)
    
    if not cached_data:
        # Calculate fresh data
        stats = calculate_company_stats(company_name)
        # Cache for 1 hour (3600 seconds)
        frappe.cache().set_value(cache_key, stats, expires_in_sec=3600)
        logger.info(f"Calculated and cached stats for company: {company_name}")
        return stats
    
    logger.debug(f"Retrieved cached stats for company: {company_name}")
    return cached_data

def calculate_company_stats(company_name):
    """Calculate company statistics"""
    try:
        stats = {
            "departments": frappe.db.count('CM Department', filters={'company': company_name}),
            "employees": frappe.db.count('CM Employee', filters={'company': company_name}),
            "projects": frappe.db.count('CM Project', filters={'company': company_name}),
            "active_projects": frappe.db.count('CM Project', filters={'company': company_name, 'status': ['!=', 'Completed']}),
            "pending_reviews": frappe.db.count('Performance Review', filters={
                'workflow_state': ['in', ['Pending Review', 'Review Scheduled', 'Under Approval']]
            })
        }
        
        # Calculate employee distribution by department
        employees_by_dept = frappe.db.sql("""
            SELECT d.department_name, COUNT(e.name) as employee_count
            FROM `tabCM Department` d 
            LEFT JOIN `tabCM Employee` e ON d.name = e.department 
            WHERE d.company = %s 
            GROUP BY d.name, d.department_name
        """, (company_name,), as_dict=True)
        
        stats["employee_distribution"] = employees_by_dept
        
        return stats
        
    except Exception as e:
        logger.error(f"Error calculating company stats for {company_name}: {str(e)}")
        return {}

def get_cached_employee_performance(employee_name):
    """Get cached employee performance data"""
    cache_key = f"employee_performance_{employee_name}"
    cached_data = frappe.cache().get_value(cache_key)
    
    if not cached_data:
        performance_data = calculate_employee_performance(employee_name)
        # Cache for 30 minutes
        frappe.cache().set_value(cache_key, performance_data, expires_in_sec=1800)
        logger.info(f"Calculated and cached performance data for employee: {employee_name}")
        return performance_data
    
    logger.debug(f"Retrieved cached performance data for employee: {employee_name}")
    return cached_data

def calculate_employee_performance(employee_name):
    """Calculate employee performance metrics"""
    try:
        # Get all performance reviews for employee
        reviews = frappe.get_all('Performance Review',
                               filters={'employee': employee_name},
                               fields=['overall_rating', 'review_period_end', 'workflow_state'],
                               order_by='review_period_end desc')
        
        performance_data = {
            "total_reviews": len(reviews),
            "latest_rating": reviews[0].get('overall_rating') if reviews else None,
            "reviews_by_year": {},
            "average_rating": 0
        }
        
        # Calculate average rating and group by year
        if reviews:
            rating_sum = 0
            rating_count = 0
            
            for review in reviews:
                if review.overall_rating and review.overall_rating.startswith(('1', '2', '3', '4', '5')):
                    rating_value = int(review.overall_rating[0])
                    rating_sum += rating_value
                    rating_count += 1
                    
                    # Group by year
                    year = review.review_period_end.year if review.review_period_end else 'Unknown'
                    if year not in performance_data["reviews_by_year"]:
                        performance_data["reviews_by_year"][year] = []
                    performance_data["reviews_by_year"][year].append(review)
            
            if rating_count > 0:
                performance_data["average_rating"] = round(rating_sum / rating_count, 2)
        
        return performance_data
        
    except Exception as e:
        logger.error(f"Error calculating performance data for {employee_name}: {str(e)}")
        return {}

def clear_cache_for_company(company_name):
    """Clear all cached data for a company"""
    cache_keys = [
        f"company_stats_{company_name}",
    ]
    
    for key in cache_keys:
        frappe.cache().delete_value(key)
    
    logger.info(f"Cleared cache for company: {company_name}")

def clear_cache_for_employee(employee_name):
    """Clear cached data for an employee"""
    cache_key = f"employee_performance_{employee_name}"
    frappe.cache().delete_value(cache_key)
    logger.info(f"Cleared cache for employee: {employee_name}")

def clear_all_company_management_cache():
    """Clear all company management related cache"""
    try:
        # Get all cache keys related to company management
        cache = frappe.cache()
        
        # This is a simplified approach - in production you'd want a more sophisticated cache key management
        companies = frappe.get_all('CM Company', pluck='name')
        employees = frappe.get_all('CM Employee', pluck='name')
        
        for company in companies:
            clear_cache_for_company(company)
            
        for employee in employees:
            clear_cache_for_employee(employee)
            
        logger.info("Cleared all company management cache")
        
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")

def get_dashboard_cache_key(user, dashboard_type):
    """Generate cache key for dashboard data"""
    return f"dashboard_{dashboard_type}_{user}_{frappe.utils.today()}"

def cache_dashboard_data(user, dashboard_type, data, expires_in_minutes=15):
    """Cache dashboard data"""
    cache_key = get_dashboard_cache_key(user, dashboard_type)
    frappe.cache().set_value(cache_key, data, expires_in_sec=expires_in_minutes * 60)
    logger.debug(f"Cached dashboard data: {cache_key}")

def get_cached_dashboard_data(user, dashboard_type):
    """Get cached dashboard data"""
    cache_key = get_dashboard_cache_key(user, dashboard_type)
    cached_data = frappe.cache().get_value(cache_key)
    
    if cached_data:
        logger.debug(f"Retrieved cached dashboard data: {cache_key}")
    
    return cached_data