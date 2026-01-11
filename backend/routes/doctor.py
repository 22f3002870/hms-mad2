from flask import Blueprint, jsonify
from utils.decorators import login_required

doctor_bp = Blueprint("doctor", __name__)

@doctor_bp.route("/dashboard")
@login_required(role="doctor")
def doctor_dashboard():
    return jsonify({"message": "Welcome Doctor"})
