import os
import logging
from datetime import timedelta

# Enable debug mode
DEBUG = True

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Secret key for session management
SECRET_KEY = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")

# Session configuration
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
SESSION_TYPE = "filesystem"
SESSION_PERMANENT = True
SESSION_USE_SIGNER = True

# In-memory database configuration (could be replaced with SQLite or other DB in the future)
DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///:memory:")

# Admin account configuration
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
