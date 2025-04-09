from flask import current_app, g
import sqlite3
import logging
from datetime import datetime

# In-memory storage for MVP
users = {}
posts = {}
comments = {}
likes = {}
admins = {}

user_id_counter = 1
post_id_counter = 1
comment_id_counter = 1
like_id_counter = 1
admin_id_counter = 1

def init_db(app):
    """Initialize the in-memory database with seed data if needed"""
    logging.debug("Initializing database...")
    
    # Create admin user
    from werkzeug.security import generate_password_hash
    global admin_id_counter
    
    admin_username = app.config.get('ADMIN_USERNAME', 'admin')
    admin_password = app.config.get('ADMIN_PASSWORD', 'admin')
    admin_email = app.config.get('ADMIN_EMAIL', 'admin@example.com')
    
    # Create admin if not exists
    if not any(admin.username == admin_username for admin in admins.values()):
        from app.database.models.admin.admin_model import Admin
        
        admin = Admin(
            id=admin_id_counter,
            username=admin_username,
            email=admin_email,
            password_hash=generate_password_hash(admin_password),
            created_at=datetime.now()
        )
        
        admins[admin_id_counter] = admin
        admin_id_counter += 1
        logging.debug(f"Admin user created: {admin_username}")

def get_db():
    """Return database connection (for future expansion)"""
    return {
        'users': users,
        'posts': posts,
        'comments': comments,
        'likes': likes,
        'admins': admins
    }

def get_next_user_id():
    """Get next available user ID"""
    global user_id_counter
    current_id = user_id_counter
    user_id_counter += 1
    return current_id

def get_next_post_id():
    """Get next available post ID"""
    global post_id_counter
    current_id = post_id_counter
    post_id_counter += 1
    return current_id

def get_next_comment_id():
    """Get next available comment ID"""
    global comment_id_counter
    current_id = comment_id_counter
    comment_id_counter += 1
    return current_id

def get_next_like_id():
    """Get next available like ID"""
    global like_id_counter
    current_id = like_id_counter
    like_id_counter += 1
    return current_id

def close_db(e=None):
    """Close database connection (for future expansion)"""
    pass
