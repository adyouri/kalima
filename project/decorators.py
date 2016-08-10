from flask import session, flash, redirect, url_for
from functools import wraps
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Please login')
            return redirect(url_for('users.login'))
    return wrap


