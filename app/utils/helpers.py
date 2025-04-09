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
    """Basic HTML sanitization"""
    if not value:
        return ""
    return re.sub(r'<[^>]*?>', '', value)

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
    app.jinja_env.globals['now'] = lambda format='%Y': datetime.datetime.now().strftime(format)
