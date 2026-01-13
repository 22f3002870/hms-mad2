from flask import Blueprint, jsonify, session, request
from datetime import datetime

from utils.decorators import login_required
from extensions import db
from models import Doctor, Patient, Appointment, Treatment

doctor_bp = Blueprint("doctor", __name__)

# ---------------------------------------------------
# DOCTOR DASHBOARD
# ---------------------------------------------------
from extensions import redis_client
import json

@doctor_bp.route("/dashboard", methods=["GET"])
@login_required(role="doctor")
def doctor_dashboard():
    user_id = session.get("user_id")
    cache_key = f"doctor:dashboard:{user_id}"

    cached = redis_client.get(cache_key)
    if cached:
        return jsonify(json.loads(cached))

    doctor = Doctor.query.filter_by(user_id=user_id).first()
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()

    result = [{
        "appointment_id": a.id,
        "patient_id": a.patient_id,
        "date": str(a.date),
        "time": str(a.time),
        "status": a.status
    } for a in appointments]

    redis_client.setex(cache_key, 60, json.dumps(result))
    return jsonify(result)



# ---------------------------------------------------
# UPDATE APPOINTMENT STATUS
# ---------------------------------------------------
@doctor_bp.route("/appointments/<int:appointment_id>/status", methods=["PUT"])
@login_required(role="doctor")
def update_appointment_status(appointment_id):
    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ["Completed", "Cancelled"]:
        return jsonify({"error": "Invalid status"}), 400

    user_id = session.get("user_id")
    doctor = Doctor.query.filter_by(user_id=user_id).first()

    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    #  Ensure doctor owns the appointment
    if appointment.doctor_id != doctor.id:
        return jsonify({"error": "Unauthorized access"}), 403

    # Prevent invalid transitions
    if appointment.status in ["Completed", "Cancelled"]:
        return jsonify({
            "error": "Cannot modify a completed or cancelled appointment"
        }), 400

    appointment.status = new_status
    db.session.commit()

    return jsonify({"message": "Appointment status updated"})


# ---------------------------------------------------
# ADD TREATMENT
# ---------------------------------------------------
@doctor_bp.route("/appointments/<int:appointment_id>/treatment", methods=["POST"])
@login_required(role="doctor")
def add_treatment(appointment_id):
    data = request.get_json()

    user_id = session.get("user_id")
    doctor = Doctor.query.filter_by(user_id=user_id).first()

    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    #  Ensure doctor owns the appointment
    if appointment.doctor_id != doctor.id:
        return jsonify({"error": "Unauthorized access"}), 403

    #  Cannot add treatment to cancelled appointment
    if appointment.status == "Cancelled":
        return jsonify({
            "error": "Cannot add treatment to cancelled appointment"
        }), 400

    #  Prevent duplicate treatment
    existing = Treatment.query.filter_by(
        appointment_id=appointment.id
    ).first()

    if existing:
        return jsonify({"error": "Treatment already exists"}), 400

    treatment = Treatment(
        appointment_id=appointment.id,
        diagnosis=data.get("diagnosis"),
        prescription=data.get("prescription"),
        notes=data.get("notes")
    )

    db.session.add(treatment)
    appointment.status = "Completed"
    db.session.commit()

    return jsonify({"message": "Treatment added successfully"})


# ---------------------------------------------------
# VIEW PATIENT HISTORY (FOR DOCTOR)
# ---------------------------------------------------
@doctor_bp.route("/patients/<int:patient_id>/history", methods=["GET"])
@login_required(role="doctor")
def patient_history(patient_id):
    user_id = session.get("user_id")
    doctor = Doctor.query.filter_by(user_id=user_id).first()

    appointments = Appointment.query.filter_by(
        patient_id=patient_id,
        doctor_id=doctor.id
    ).all()

    result = []
    for a in appointments:
        treatment = Treatment.query.filter_by(
            appointment_id=a.id
        ).first()

        result.append({
            "appointment_id": a.id,
            "date": str(a.date),
            "status": a.status,
            "diagnosis": treatment.diagnosis if treatment else None,
            "prescription": treatment.prescription if treatment else None,
            "notes": treatment.notes if treatment else None
        })

    return jsonify(result)
