import re
import datetime
from functools import wraps
from flask import session, flash, redirect, url_for, request, current_app

def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
    """Format a datetime object to string"""
    if value is None:
        return ""
    return value.strftime(format)

def get_current_year():
    """Return current year for copyright notices"""
    return datetime.datetime.now().year

def nl2br(value):
    """Convert newlines to <br> tags"""
    if not value:
        return ""
    return value.replace('\n', '<br>')

def truncate_text(text, length=100, ellipsis='...'):
    """Truncate text to specified length and add ellipsis"""
    if not text or len(text) <= length:
        return text
    return text[:length].rsplit(' ', 1)[0] + ellipsis

def sanitize_html(value):
    """Enhanced HTML sanitization to prevent XSS attacks"""
    if not value:
        return ""
    
    # First pass: Remove all HTML tags
    value = re.sub(r'<[^>]*?>', '', value)
    
    # Convert special characters to HTML entities
    value = value.replace('&', '&amp;')
    value = value.replace('<', '&lt;')
    value = value.replace('>', '&gt;')
    value = value.replace('"', '&quot;')
    value = value.replace("'", '&#x27;')
    value = value.replace('/', '&#x2F;')
    
    # Remove potentially dangerous patterns
    value = re.sub(r'javascript:', '', value, flags=re.IGNORECASE)
    value = re.sub(r'data:', '', value, flags=re.IGNORECASE)
    value = re.sub(r'vbscript:', '', value, flags=re.IGNORECASE)
    value = re.sub(r'on\w+\s*=', '', value, flags=re.IGNORECASE)
    value = re.sub(r'expression\s*\(', '', value, flags=re.IGNORECASE)
    value = re.sub(r'url\s*\(', 'url(', value, flags=re.IGNORECASE)  # Normalize url() calls
    
    # Remove excessive whitespace
    value = re.sub(r'\s+', ' ', value).strip()
    
    return value

def is_valid_url(url):
    """Basic URL validation"""
    if not url:
        return False
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ipv4
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def register_template_filters(app):
    """Register custom template filters with Flask app"""
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['nl2br'] = nl2br
    app.jinja_env.filters['truncate'] = truncate_text
    app.jinja_env.filters['sanitize'] = sanitize_html
    app.jinja_env.globals['now'] = lambda format='%Y': datetime.datetime.now().strftime(format)
