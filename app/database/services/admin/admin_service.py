from app.database.database import get_db
from app.database.models.admin.admin_model import Admin

class AdminService:
    """Service for admin-related operations"""
    
    def __init__(self):
        self.db = get_db()
        self.admins = self.db['admins']
    
    def get_admin_by_id(self, admin_id):
        """Get admin by ID"""
        return self.admins.get(admin_id)
    
    def get_admin_by_username(self, username):
        """Get admin by username"""
        for admin in self.admins.values():
            if admin.username == username:
                return admin
        return None
    
    def get_admin_by_email(self, email):
        """Get admin by email"""
        for admin in self.admins.values():
            if admin.email == email:
                return admin
        return None
    
    def get_all_admins(self):
        """Get all admins"""
        return list(self.admins.values())
