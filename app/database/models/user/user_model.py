class User:
    """User model for application users"""
    
    def __init__(self, id, username, email, password_hash, bio='', avatar='', 
                 created_at=None, is_active=True):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.bio = bio
        self.avatar = avatar
        self.created_at = created_at
        self.is_active = is_active
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'bio': self.bio,
            'avatar': self.avatar,
            'created_at': self.created_at,
            'is_active': self.is_active
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create user object from dictionary"""
        return cls(
            id=data.get('id'),
            username=data.get('username'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            bio=data.get('bio', ''),
            avatar=data.get('avatar', ''),
            created_at=data.get('created_at'),
            is_active=data.get('is_active', True)
        )

class Like:
    """Like model for post likes"""
    
    def __init__(self, id, user_id, post_id, created_at):
        self.id = id
        self.user_id = user_id
        self.post_id = post_id
        self.created_at = created_at
    
    def to_dict(self):
        """Convert like object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create like object from dictionary"""
        return cls(
            id=data.get('id'),
            user_id=data.get('user_id'),
            post_id=data.get('post_id'),
            created_at=data.get('created_at')
        )

class Comment:
    """Comment model for post comments"""
    
    def __init__(self, id, user_id, post_id, content, created_at):
        self.id = id
        self.user_id = user_id
        self.post_id = post_id
        self.content = content
        self.created_at = created_at
    
    def to_dict(self):
        """Convert comment object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'content': self.content,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create comment object from dictionary"""
        return cls(
            id=data.get('id'),
            user_id=data.get('user_id'),
            post_id=data.get('post_id'),
            content=data.get('content'),
            created_at=data.get('created_at')
        )
