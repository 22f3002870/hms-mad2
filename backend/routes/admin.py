from flask import Blueprint, jsonify
from utils.decorators import login_required
from models import Doctor, Patient, Appointment

admin_bp = Blueprint("admin", __name__)

from extensions import redis_client
import json

@admin_bp.route("/dashboard", methods=["GET"])
@login_required(role="admin")
def admin_dashboard():
    cache_key = "admin:dashboard"

    cached = redis_client.get(cache_key)
    if cached:
        return jsonify(json.loads(cached))

    data = {
        "total_doctors": Doctor.query.count(),
        "total_patients": Patient.query.count(),
        "total_appointments": Appointment.query.count()
    }

    redis_client.setex(cache_key, 120, json.dumps(data))
    return jsonify(data)

from flask import request
from models import User, Doctor
from extensions import db

@admin_bp.route("/doctors", methods=["POST"])
@login_required(role="admin")
def add_doctor():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    user = User(
        name=data["name"],
        email=data["email"],
        role="doctor"
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    doctor = Doctor(
        user_id=user.id,
        department_id=data.get("department_id")
    )
    db.session.add(doctor)
    db.session.commit()

    return jsonify({"message": "Doctor added successfully"})

@admin_bp.route("/doctors", methods=["GET"])
@login_required(role="admin")
def list_doctors():
    doctors = Doctor.query.all()

    result = []
    for d in doctors:
        result.append({
            "doctor_id": d.id,
            "user_id": d.user_id,
            "department_id": d.department_id,
            "is_available": d.is_available
        })

    return jsonify(result)

@admin_bp.route("/patients", methods=["GET"])
@login_required(role="admin")
def search_patients():
    query = request.args.get("query", "")

    patients = Patient.query.filter(
        Patient.id.like(f"%{query}%")
    ).all()

    result = []
    for p in patients:
        result.append({
            "patient_id": p.id,
            "user_id": p.user_id,
            "age": p.age
        })

    return jsonify(result)

from models import Appointment

@admin_bp.route("/appointments", methods=["GET"])
@login_required(role="admin")
def view_appointments():
    appointments = Appointment.query.all()

    result = []
    for a in appointments:
        result.append({
            "appointment_id": a.id,
            "doctor_id": a.doctor_id,
            "patient_id": a.patient_id,
            "date": str(a.date),
            "time": str(a.time),
            "status": a.status
        })

    return jsonify(result)
