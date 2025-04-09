from app.database.services.user.user_service import UserService
from app.database.services.user.post_service import PostService

class UserContainer:
    """Container for user-related services"""
    
    def __init__(self):
        self.user_service = UserService()
        self.post_service = PostService()
    
    def get_user_service(self):
        """Get user service instance"""
        return self.user_service
    
    def get_post_service(self):
        """Get post service instance"""
        return self.post_service
