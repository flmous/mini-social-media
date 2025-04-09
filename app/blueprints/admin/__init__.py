from flask import Blueprint

admin_bp = Blueprint('admin', __name__, template_folder='../../templates/admin', static_folder='../../static/admin')

from app.blueprints.admin.routes import *
