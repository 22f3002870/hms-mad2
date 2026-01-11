from functools import wraps
from flask import session, redirect, url_for, abort

def login_required(role=None):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if "user_id" not in session:
                return redirect("/login")

            if role and session.get("role") != role:
                abort(403)

            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
