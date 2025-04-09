import os
import logging
from datetime import timedelta

# Debug mode based on environment
DEBUG = os.environ.get('FLASK_ENV', 'production') != 'production'

# Configure logging based on environment
log_level = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Secret key for session management (use a secure key in production)
if os.environ.get('FLASK_ENV') == 'production' and not os.environ.get('SESSION_SECRET'):
    logging.warning("No SESSION_SECRET set in production environment. Using a random key that will change on restart.")
SECRET_KEY = os.environ.get("SESSION_SECRET", os.urandom(24).hex())

# Session configuration
PERMANENT_SESSION_LIFETIME = timedelta(days=7)  # How long a user session lasts before requiring re-login
SESSION_TYPE = "filesystem"  # Store session data on the filesystem
SESSION_PERMANENT = True  # Keep the session active for PERMANENT_SESSION_LIFETIME
SESSION_USE_SIGNER = True  # Sign the session cookie for extra security

# Security-related cookie settings
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript from accessing the session cookie (prevents XSS)
SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'  # Only send cookie over HTTPS in production
SESSION_COOKIE_SAMESITE = 'Lax'  # Prevents CSRF attacks by limiting cross-site requests

# In-memory database configuration (could be replaced with SQLite or other DB in the future)
DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///:memory:")

# Admin account configuration
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
