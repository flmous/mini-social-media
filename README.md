# Mini Social Media Platform

A modular mini social media website built with Flask, featuring user and admin functionalities, organized with blueprints. This application follows best practices for security, performance, and maintainability.

## Features

- **User Authentication**: Register, login, and manage user profiles
- **Social Media Features**: Create posts, like posts, comment on posts
- **Profile Management**: Edit profile information, view other user profiles
- **Admin Panel**: Moderate content, manage users, view statistics
- **Responsive Design**: Works well on desktop and mobile devices
- **Security**: CSRF protection, content sanitization, XSS protection, secure cookies
- **Performance**: Caching strategies for static content, optimized database queries

## Technology Stack

- **Backend**: Python with Flask framework
- **Frontend**: HTML, CSS, JavaScript with Bootstrap
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF with CSRF protection
- **Database**: In-memory storage with SQLAlchemy-compatible interface (expandable to SQL databases)
- **Templating**: Jinja2 with custom filters for content formatting and security

## Project Structure

The application follows a modular design with Flask blueprints:

- **User Module**: Handles user-related features like posts, comments, and profiles
- **Admin Module**: Provides administrative functions for content moderation
- **Database Layer**: Separated into models, services, and containers for better maintainability

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/mini-social-media.git
cd mini-social-media
```

2. Set up virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Configure environment variables:
```
cp .env.example .env
# Edit the .env file with your configuration
```

5. Run the application:
```
flask run
```

6. Visit `http://localhost:5000` in your browser

### Configuration

The application can be configured through environment variables:

- `FLASK_ENV`: Set to 'production' for production environment
- `SESSION_SECRET`: Secret key for session management
- `DATABASE_URL`: Database connection URL
- `ADMIN_USERNAME`: Admin account username
- `ADMIN_PASSWORD`: Admin account password
- `ADMIN_EMAIL`: Admin account email

## Development

### Running in Debug Mode

```
FLASK_ENV=development flask run
```

### Project Structure Guidelines

- New features should be added as separate modules in the appropriate blueprint
- Database models should be placed in `app/database/models`
- Services should be placed in `app/database/services`

### Security Best Practices

This application implements several security best practices:

1. **CSRF Protection**: All forms are protected against Cross-Site Request Forgery attacks
2. **Content Sanitization**: User-generated content is sanitized to prevent XSS attacks
3. **Secure Cookies**: HTTP-only cookies with SameSite policy
4. **HTTPS Enforcement**: In production, cookies are only sent over HTTPS
5. **Password Security**: Passwords are hashed securely, never stored in plaintext

### Performance Considerations

The application includes several performance optimizations:

1. **Static Asset Caching**: Long-lived cache headers for static assets
2. **Efficient Database Queries**: Minimized database calls with caching where appropriate
3. **Optimized Templates**: Templates use inheritance to reduce duplication

## Deployment

For production deployment, ensure you:

1. Generate a strong random key for `SESSION_SECRET`
2. Use a production-grade database (PostgreSQL recommended)
3. Set up HTTPS with a valid SSL certificate
4. Configure proper logging
5. Change default admin credentials

## License

[MIT License](LICENSE)