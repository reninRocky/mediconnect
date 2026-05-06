from __future__ import annotations

from functools import wraps

from flask import abort
from flask_login import current_user, login_required


def role_required(*roles: str):
    def decorator(fn):
        @wraps(fn)
        @login_required
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if roles and getattr(current_user, "role", None) not in roles:
                abort(403)
            return fn(*args, **kwargs)

        return wrapper

    return decorator

