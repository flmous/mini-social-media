from functools import wraps
from flask import session, flash, redirect, url_for, request, current_app

def login_required(f):
    """Decorator to require user login for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('user.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_login_required(f):
    """Decorator to require admin login for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Admin access required.', 'warning')
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to verify if logged in user is an admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('user.login', next=request.url))
        
        from app.database.services.admin.admin_service import AdminService
        admin_service = AdminService()
        
        # Check if current user is an admin
        user_id = session.get('user_id')
        admin = admin_service.get_admin_by_id(user_id)
        
        if not admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('user.feed'))
            
        return f(*args, **kwargs)
    return decorated_function

def is_authenticated():
    """Check if a user is authenticated"""
    return 'user_id' in session

def is_admin():
    """Check if current user is an admin"""
    if 'admin_id' in session:
        return True
    return False

def get_current_user_id():
    """Get the current user's ID"""
    return session.get('user_id')
