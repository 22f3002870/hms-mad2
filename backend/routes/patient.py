from flask import Blueprint, request, jsonify
from models import User, Patient
from extensions import db

patient_bp = Blueprint("patient", __name__)

@patient_bp.route("/register", methods=["POST"])
def register_patient():
    data = request.json

    user = User(
        name=data["name"],
        email=data["email"],
        role="patient"
    )
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    patient = Patient(
        user_id=user.id,
        age=data.get("age")
    )
    db.session.add(patient)
    db.session.commit()

    return jsonify({"message": "Patient registered successfully"})

from utils.decorators import login_required

@patient_bp.route("/dashboard")
@login_required(role="patient")
def patient_dashboard():
    return jsonify({"message": "Welcome Patient"})
