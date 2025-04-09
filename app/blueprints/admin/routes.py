from flask import render_template, redirect, url_for, request, flash, session
from app.blueprints.admin import admin_bp
from app.blueprints.admin.forms import AdminLoginForm
from app.database.services.admin.admin_service import AdminService
from app.database.services.user.user_service import UserService
from app.database.services.user.post_service import PostService
from app.security.auth import admin_required, admin_login_required
from werkzeug.security import check_password_hash

admin_service = AdminService()
user_service = UserService()
post_service = PostService()

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@admin_login_required
def dashboard():
    """Admin dashboard with overview statistics"""
    user_count = user_service.get_user_count()
    post_count = post_service.get_post_count()
    recent_users = user_service.get_recent_users(5)
    recent_posts = post_service.get_recent_posts(5)
    
    return render_template('admin/dashboard.html', 
                          user_count=user_count, 
                          post_count=post_count,
                          recent_users=recent_users,
                          recent_posts=recent_posts)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if 'admin_id' in session:
        return redirect(url_for('admin.dashboard'))
    
    form = AdminLoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        admin = admin_service.get_admin_by_username(username)
        
        if admin and check_password_hash(admin.password_hash, password):
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            flash('Login successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('admin/login.html', form=form)

@admin_bp.route('/logout')
@admin_login_required
def logout():
    """Admin logout"""
    session.pop('admin_id', None)
    session.pop('admin_username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('admin.login'))

@admin_bp.route('/users')
@admin_login_required
def users():
    """List all users for admin management"""
    users_list = user_service.get_all_users()
    return render_template('admin/users.html', users=users_list)

@admin_bp.route('/user/<int:user_id>')
@admin_login_required
def user_detail(user_id):
    """View user details and their posts"""
    user = user_service.get_user_by_id(user_id)
    posts = post_service.get_posts_by_user_id(user_id)
    
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/user_detail.html', user=user, posts=posts)

@admin_bp.route('/posts')
@admin_login_required
def posts():
    """List all posts for admin moderation"""
    posts_list = post_service.get_all_posts()
    return render_template('admin/posts.html', posts=posts_list)

@admin_bp.route('/post/<int:post_id>')
@admin_login_required
def post_detail(post_id):
    """View post details for moderation"""
    post = post_service.get_post_by_id(post_id)
    
    if not post:
        flash('Post not found', 'danger')
        return redirect(url_for('admin.posts'))
    
    return render_template('admin/post_detail.html', post=post)

@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@admin_login_required
def delete_post(post_id):
    """Delete a post"""
    result = post_service.delete_post(post_id)
    
    if result:
        flash('Post deleted successfully', 'success')
    else:
        flash('Failed to delete post', 'danger')
    
    return redirect(url_for('admin.posts'))

@admin_bp.route('/user/<int:user_id>/toggle_status', methods=['POST'])
@admin_login_required
def toggle_user_status(user_id):
    """Toggle user active/inactive status"""
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('admin.users'))
    
    new_status = not user.is_active
    result = user_service.update_user_status(user_id, new_status)
    
    if result:
        action = "activated" if new_status else "deactivated"
        flash(f'User {action} successfully', 'success')
    else:
        flash('Failed to update user status', 'danger')
    
    return redirect(url_for('admin.users'))
