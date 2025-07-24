# decorators.py
from functools import wraps
from flask import session, redirect, url_for, flash

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('role'):
            flash("Please log in first.", "warning")
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash("Admin access only.", "danger")
            return redirect(url_for('dashboard'))
        return func(*args, **kwargs)
    return wrapper


def role_required(role_name):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not session.get('role'):
                flash("Please login first.", "warning")
                return redirect(url_for('login'))
            if session.get('role') != role_name:
                flash("Unauthorized access.", "danger")
                return redirect(url_for('dashboard'))
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
