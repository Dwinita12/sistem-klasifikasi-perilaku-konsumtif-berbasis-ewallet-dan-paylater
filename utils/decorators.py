from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "username" not in session:
            flash("Silakan login dulu")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrap