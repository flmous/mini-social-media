from flask import render_template, redirect, url_for, request, flash, session
from app.blueprints.user import user_bp
from app.blueprints.user.forms import RegisterForm, LoginForm, ProfileForm, PostForm, CommentForm
from app.database.services.user.user_service import UserService
from app.database.services.user.post_service import PostService
from app.security.auth import login_required
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

user_service = UserService()
post_service = PostService()

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if 'user_id' in session:
        return redirect(url_for('user.feed'))
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # Check if username or email already exists
        if user_service.get_user_by_username(username):
            flash('Username already exists', 'danger')
            return render_template('user/register.html', form=form)
        
        if user_service.get_user_by_email(email):
            flash('Email already registered', 'danger')
            return render_template('user/register.html', form=form)
        
        # Create new user
        password_hash = generate_password_hash(password)
        user_data = {
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'bio': '',
            'avatar': '',
            'created_at': datetime.now(),
            'is_active': True
        }
        
        user_id = user_service.create_user(user_data)
        
        if user_id:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('user.login'))
        else:
            flash('Registration failed. Please try again.', 'danger')
    
    return render_template('user/register.html', form=form)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if 'user_id' in session:
        return redirect(url_for('user.feed'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = user_service.get_user_by_username(username)
        
        if user and check_password_hash(user.password_hash, password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact admin.', 'danger')
                return render_template('user/login.html', form=form)
            
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('user.feed'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('user/login.html', form=form)

@user_bp.route('/logout')
def logout():
    """User logout"""
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('user.login'))

@user_bp.route('/feed')
@login_required
def feed():
    """User feed showing all posts"""
    posts = post_service.get_all_posts()
    user_id = session.get('user_id')
    user = user_service.get_user_by_id(user_id)
    return render_template('user/feed.html', posts=posts, user=user, user_service=user_service)

@user_bp.route('/profile')
@login_required
def profile():
    """Current user's profile"""
    user_id = session.get('user_id')
    user = user_service.get_user_by_id(user_id)
    user_posts = post_service.get_posts_by_user_id(user_id)
    
    return render_template('user/profile.html', user=user, posts=user_posts)

@user_bp.route('/profile/<int:user_id>')
@login_required
def view_profile(user_id):
    """View another user's profile"""
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('user.feed'))
    
    user_posts = post_service.get_posts_by_user_id(user_id)
    
    return render_template('user/profile.html', user=user, posts=user_posts, is_own_profile=False)

@user_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit current user's profile"""
    user_id = session.get('user_id')
    user = user_service.get_user_by_id(user_id)
    
    form = ProfileForm(obj=user)
    
    if form.validate_on_submit():
        user_data = {
            'username': form.username.data,
            'email': form.email.data,
            'bio': form.bio.data,
            'avatar': form.avatar.data
        }
        
        # Check if username is changed and already exists
        if user.username != user_data['username'] and user_service.get_user_by_username(user_data['username']):
            flash('Username already exists', 'danger')
            return render_template('user/edit_profile.html', form=form)
        
        # Check if email is changed and already exists
        if user.email != user_data['email'] and user_service.get_user_by_email(user_data['email']):
            flash('Email already registered', 'danger')
            return render_template('user/edit_profile.html', form=form)
        
        result = user_service.update_user(user_id, user_data)
        
        if result:
            # Update session data if username changed
            if user.username != user_data['username']:
                session['username'] = user_data['username']
            
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('user.profile'))
        else:
            flash('Failed to update profile', 'danger')
    
    return render_template('user/edit_profile.html', form=form)

@user_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    """Create a new post"""
    form = PostForm()
    
    if form.validate_on_submit():
        user_id = session.get('user_id')
        
        post_data = {
            'user_id': user_id,
            'content': form.content.data,
            'created_at': datetime.now()
        }
        
        post_id = post_service.create_post(post_data)
        
        if post_id:
            flash('Post created successfully!', 'success')
            return redirect(url_for('user.feed'))
        else:
            flash('Failed to create post', 'danger')
    
    return render_template('user/new_post.html', form=form)

@user_bp.route('/post/<int:post_id>')
@login_required
def post_detail(post_id):
    """View a specific post with comments"""
    post = post_service.get_post_by_id(post_id)
    
    if not post:
        flash('Post not found', 'danger')
        return redirect(url_for('user.feed'))
    
    comments = post_service.get_comments_by_post_id(post_id)
    form = CommentForm()
    
    return render_template('user/post_detail.html', post=post, comments=comments, form=form)

@user_bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    """Add a comment to a post"""
    form = CommentForm()
    
    if form.validate_on_submit():
        user_id = session.get('user_id')
        
        comment_data = {
            'user_id': user_id,
            'post_id': post_id,
            'content': form.content.data,
            'created_at': datetime.now()
        }
        
        comment_id = post_service.create_comment(comment_data)
        
        if comment_id:
            flash('Comment added successfully!', 'success')
        else:
            flash('Failed to add comment', 'danger')
    
    return redirect(url_for('user.post_detail', post_id=post_id))

@user_bp.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    """Like or unlike a post"""
    user_id = session.get('user_id')
    
    # Check if user already liked the post
    if post_service.user_liked_post(user_id, post_id):
        # Unlike the post
        result = post_service.unlike_post(user_id, post_id)
        message = 'Post unliked'
    else:
        # Like the post
        result = post_service.like_post(user_id, post_id)
        message = 'Post liked'
    
    if result:
        flash(message, 'success')
    else:
        flash('Failed to update like status', 'danger')
    
    # Get the referer URL to redirect back to the appropriate page
    referer = request.headers.get('Referer')
    if referer:
        return redirect(referer)
    return redirect(url_for('user.feed'))

@user_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete a post (only by the author)"""
    user_id = session.get('user_id')
    post = post_service.get_post_by_id(post_id)
    
    if not post:
        flash('Post not found', 'danger')
        return redirect(url_for('user.feed'))
    
    # Check if user is the author of the post
    if post.user_id != user_id:
        flash('You can only delete your own posts', 'danger')
        return redirect(url_for('user.post_detail', post_id=post_id))
    
    result = post_service.delete_post(post_id)
    
    if result:
        flash('Post deleted successfully', 'success')
        return redirect(url_for('user.profile'))
    else:
        flash('Failed to delete post', 'danger')
        return redirect(url_for('user.post_detail', post_id=post_id))
