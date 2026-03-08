from flask import Blueprint, request, jsonify
from models import User
from extensions import db
import uuid

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST", "OPTIONS"])
def login():
    # ✅ ALWAYS allow preflight
    if request.method == "OPTIONS":
        return jsonify({}), 200

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email, is_active=True).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = str(uuid.uuid4())
    user.token = token
    db.session.commit()

    return jsonify({
        "token": token,
        "role": user.role
    })


@auth_bp.route("/logout", methods=["POST"])
def logout():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token missing"}), 401

    user = User.query.filter_by(token=token).first()
    if user:
        user.token = None
        db.session.commit()

    return jsonify({"message": "Logged out successfully"})
