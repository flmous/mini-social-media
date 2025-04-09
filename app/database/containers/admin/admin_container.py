from app.database.services.admin.admin_service import AdminService

class AdminContainer:
    """Container for admin-related services"""
    
    def __init__(self):
        self.admin_service = AdminService()
    
    def get_admin_service(self):
        """Get admin service instance"""
        return self.admin_service
