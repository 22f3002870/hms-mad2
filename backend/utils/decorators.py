from functools import wraps
from flask import request, jsonify
from models import User

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            # ✅ Allow preflight requests
            if request.method == "OPTIONS":
                return "", 200

            token = request.headers.get("Authorization")

            if not token:
                return jsonify({"error": "Missing token"}), 401

            user = User.query.filter_by(token=token).first()
            if not user:
                return jsonify({"error": "Invalid token"}), 401

            if role and user.role != role:
                return jsonify({"error": "Unauthorized"}), 403

            # ✅ Attach user info to request
            request.user_id = user.id
            request.user_role = user.role

            return f(*args, **kwargs)

        return wrapper
    return decorator
