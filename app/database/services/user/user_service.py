from app.database.database import get_db, get_next_user_id
from app.database.models.user.user_model import User
from datetime import datetime

class UserService:
    """Service for user-related operations"""
    
    def __init__(self):
        self.db = get_db()
        self.users = self.db['users']
    
    def create_user(self, user_data):
        """Create a new user"""
        user_id = get_next_user_id()
        user_data['id'] = user_id
        
        user = User.from_dict(user_data)
        self.users[user_id] = user
        
        return user_id
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_user_by_username(self, username):
        """Get user by username"""
        for user in self.users.values():
            if user.username == username:
                return user
        return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        for user in self.users.values():
            if user.email == email:
                return user
        return None
    
    def get_all_users(self):
        """Get all users"""
        return list(self.users.values())
    
    def update_user(self, user_id, user_data):
        """Update user information"""
        user = self.get_user_by_id(user_id)
        
        if not user:
            return False
        
        # Update user fields
        if 'username' in user_data:
            user.username = user_data['username']
        if 'email' in user_data:
            user.email = user_data['email']
        if 'bio' in user_data:
            user.bio = user_data['bio']
        if 'avatar' in user_data:
            user.avatar = user_data['avatar']
        if 'password_hash' in user_data:
            user.password_hash = user_data['password_hash']
        
        return True
    
    def update_user_status(self, user_id, is_active):
        """Update user active status"""
        user = self.get_user_by_id(user_id)
        
        if not user:
            return False
        
        user.is_active = is_active
        return True
    
    def delete_user(self, user_id):
        """Delete a user"""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
    
    def get_user_count(self):
        """Get total number of users"""
        return len(self.users)
    
    def get_recent_users(self, limit=5):
        """Get recently registered users"""
        users_list = list(self.users.values())
        # Sort by creation date (newest first)
        users_list.sort(key=lambda x: x.created_at, reverse=True)
        return users_list[:limit]
