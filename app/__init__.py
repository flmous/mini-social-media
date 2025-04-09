import os
import logging
import sys
from flask import Flask, request
from flask_wtf.csrf import CSRFProtect
from config import *

# Initialize csrf protection
csrf = CSRFProtect()

def create_app():
    """Initialize and configure the Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('config')
    app.secret_key = SECRET_KEY
    
    # Initialize CSRF protection
    csrf.init_app(app)
    
    # Configure application logging
    if not app.debug:
        # Log to stderr
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)
        
    # Log application startup
    app.logger.info('Mini Social Media Application Startup')
    
    # Add request logging for production
    @app.before_request
    def log_request():
        if not app.debug:
            # Don't log static file requests
            if not request.path.startswith('/static/'):
                app.logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")
    
    # Add security headers
    @app.after_request
    def add_security_headers(response):
        # Enable HTTP Strict Transport Security (HSTS)
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        # Enable XSS protection in browsers
        response.headers['X-XSS-Protection'] = '1; mode=block'
        # Prevent clickjacking attacks
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        # Control cross-origin resource sharing
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    
    # Import and register blueprints
    from app.blueprints.user import user_bp
    from app.blueprints.admin import admin_bp
    
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Import and initialize database
    from app.database.database import init_db
    init_db(app)
    
    # Register template filters
    from app.utils.helpers import register_template_filters
    register_template_filters(app)
    
    # Register error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        app.logger.warning(f"Page not found: {request.path}")
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        app.logger.error(f"Internal Server Error: {str(e)}")
        return render_template('500.html'), 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Log the error and stacktrace
        app.logger.error(f"Unhandled Exception: {str(e)}", exc_info=True)
        return render_template('500.html'), 500
    
    # Route to homepage
    @app.route('/')
    def index():
        return redirect(url_for('user.feed'))
    
    return app

# Import these here to avoid circular imports
from flask import render_template, redirect, url_for
