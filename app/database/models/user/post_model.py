class Post:
    """Post model for user posts"""
    
    def __init__(self, id, user_id, content, created_at):
        self.id = id
        self.user_id = user_id
        self.content = content
        self.created_at = created_at
        self.like_count = 0  # Dynamic value, not stored in database
    
    def to_dict(self):
        """Convert post object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'created_at': self.created_at,
            'like_count': self.like_count
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create post object from dictionary"""
        post = cls(
            id=data.get('id'),
            user_id=data.get('user_id'),
            content=data.get('content'),
            created_at=data.get('created_at')
        )
        post.like_count = data.get('like_count', 0)
        return post
