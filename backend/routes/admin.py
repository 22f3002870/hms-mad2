from flask import Blueprint, jsonify
from utils.decorators import login_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard")
@login_required(role="admin")
def admin_dashboard():
    return jsonify({"message": "Welcome Admin"})
