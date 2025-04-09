from app.database.database import get_db, get_next_post_id, get_next_comment_id, get_next_like_id
from app.database.models.user.post_model import Post
from app.database.models.user.user_model import Comment, Like
from datetime import datetime

class PostService:
    """Service for post-related operations"""
    
    def __init__(self):
        self.db = get_db()
        self.posts = self.db['posts']
        self.comments = self.db['comments']
        self.likes = self.db['likes']
        self.users = self.db['users']
    
    def create_post(self, post_data):
        """Create a new post"""
        post_id = get_next_post_id()
        post_data['id'] = post_id
        
        post = Post.from_dict(post_data)
        self.posts[post_id] = post
        
        return post_id
    
    def get_post_by_id(self, post_id):
        """Get post by ID with like count"""
        post = self.posts.get(post_id)
        
        if post:
            # Calculate like count
            post.like_count = self.get_post_like_count(post_id)
            
            # Add username to post
            post.username = self.users.get(post.user_id).username if post.user_id in self.users else "Unknown"
        
        return post
    
    def get_all_posts(self):
        """Get all posts with like counts and usernames"""
        posts_list = list(self.posts.values())
        
        # Calculate like count for each post and add username
        for post in posts_list:
            post.like_count = self.get_post_like_count(post.id)
            post.username = self.users.get(post.user_id).username if post.user_id in self.users else "Unknown"
        
        # Sort by creation date (newest first)
        posts_list.sort(key=lambda x: x.created_at, reverse=True)
        
        return posts_list
    
    def get_posts_by_user_id(self, user_id):
        """Get posts by user ID"""
        user_posts = [post for post in self.posts.values() if post.user_id == user_id]
        
        # Calculate like count for each post
        for post in user_posts:
            post.like_count = self.get_post_like_count(post.id)
            post.username = self.users.get(post.user_id).username if post.user_id in self.users else "Unknown"
        
        # Sort by creation date (newest first)
        user_posts.sort(key=lambda x: x.created_at, reverse=True)
        
        return user_posts
    
    def update_post(self, post_id, post_data):
        """Update post content"""
        post = self.get_post_by_id(post_id)
        
        if not post:
            return False
        
        # Update post fields
        if 'content' in post_data:
            post.content = post_data['content']
        
        return True
    
    def delete_post(self, post_id):
        """Delete a post and its associated comments and likes"""
        if post_id not in self.posts:
            return False
        
        # Delete associated comments
        self.comments = {k: v for k, v in self.comments.items() if v.post_id != post_id}
        
        # Delete associated likes
        self.likes = {k: v for k, v in self.likes.items() if v.post_id != post_id}
        
        # Delete the post
        del self.posts[post_id]
        
        return True
    
    def create_comment(self, comment_data):
        """Create a new comment"""
        comment_id = get_next_comment_id()
        comment_data['id'] = comment_id
        
        comment = Comment.from_dict(comment_data)
        self.comments[comment_id] = comment
        
        return comment_id
    
    def get_comments_by_post_id(self, post_id):
        """Get comments for a post with user information"""
        post_comments = [comment for comment in self.comments.values() if comment.post_id == post_id]
        
        # Add username to each comment
        for comment in post_comments:
            comment.username = self.users.get(comment.user_id).username if comment.user_id in self.users else "Unknown"
        
        # Sort by creation date (oldest first for comments)
        post_comments.sort(key=lambda x: x.created_at)
        
        return post_comments
    
    def like_post(self, user_id, post_id):
        """Add a like to a post"""
        # Check if post exists
        if post_id not in self.posts:
            return False
        
        # Check if user already liked the post
        if self.user_liked_post(user_id, post_id):
            return False
        
        # Create new like
        like_id = get_next_like_id()
        like = Like(
            id=like_id,
            user_id=user_id,
            post_id=post_id,
            created_at=datetime.now()
        )
        
        self.likes[like_id] = like
        
        return True
    
    def unlike_post(self, user_id, post_id):
        """Remove a like from a post"""
        # Find the like
        for like_id, like in self.likes.items():
            if like.user_id == user_id and like.post_id == post_id:
                # Remove the like
                del self.likes[like_id]
                return True
        
        return False
    
    def user_liked_post(self, user_id, post_id):
        """Check if a user liked a post"""
        for like in self.likes.values():
            if like.user_id == user_id and like.post_id == post_id:
                return True
        
        return False
    
    def get_post_like_count(self, post_id):
        """Get number of likes for a post"""
        return sum(1 for like in self.likes.values() if like.post_id == post_id)
    
    def get_post_count(self):
        """Get total number of posts"""
        return len(self.posts)
    
    def get_recent_posts(self, limit=5):
        """Get recently created posts"""
        posts_list = list(self.posts.values())
        
        # Add username to each post
        for post in posts_list:
            post.username = self.users.get(post.user_id).username if post.user_id in self.users else "Unknown"
        
        # Sort by creation date (newest first)
        posts_list.sort(key=lambda x: x.created_at, reverse=True)
        
        return posts_list[:limit]
