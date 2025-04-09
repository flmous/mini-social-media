import os
import logging
from flask import Flask
from config import *

def create_app():
    """Initialize and configure the Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('config')
    app.secret_key = SECRET_KEY
    
    # Import and register blueprints
    from app.blueprints.user import user_bp
    from app.blueprints.admin import admin_bp
    
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Import and initialize database
    from app.database.database import init_db
    init_db(app)
    
    # Register error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
    
    # Route to homepage
    @app.route('/')
    def index():
        return redirect(url_for('user.feed'))
    
    return app

# Import these here to avoid circular imports
from flask import render_template, redirect, url_for
