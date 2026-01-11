from flask import Blueprint, jsonify, session
from utils.decorators import login_required
from models import Doctor, Appointment

doctor_bp = Blueprint("doctor", __name__)

@doctor_bp.route("/dashboard", methods=["GET"])
@login_required(role="doctor")
def doctor_dashboard():
    user_id = session.get("user_id")

    doctor = Doctor.query.filter_by(user_id=user_id).first()
    if not doctor:
        return jsonify({"error": "Doctor profile not found"}), 404

    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()

    result = []
    for a in appointments:
        result.append({
            "appointment_id": a.id,
            "patient_id": a.patient_id,
            "date": str(a.date),
            "time": str(a.time),
            "status": a.status
        })

    return jsonify(result)


from flask import request
from extensions import db

@doctor_bp.route("/appointments/<int:appointment_id>/status", methods=["PUT"])
@login_required(role="doctor")
def update_appointment_status(appointment_id):
    data = request.get_json()
    status = data.get("status")

    if status not in ["Booked", "Completed", "Cancelled"]:
        return jsonify({"error": "Invalid status"}), 400

    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    appointment.status = status
    db.session.commit()

    return jsonify({"message": "Appointment status updated"})


from models import Treatment
from datetime import datetime

@doctor_bp.route("/appointments/<int:appointment_id>/treatment", methods=["POST"])
@login_required(role="doctor")
def add_treatment(appointment_id):
    data = request.get_json()

    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    treatment = Treatment(
        appointment_id=appointment.id,
        diagnosis=data.get("diagnosis"),
        prescription=data.get("prescription"),
        notes=data.get("notes"),
        
    )

    db.session.add(treatment)
    appointment.status = "Completed"
    db.session.commit()

    return jsonify({"message": "Treatment added successfully"})


from models import Patient

@doctor_bp.route("/patients/<int:patient_id>/history", methods=["GET"])
@login_required(role="doctor")
def patient_history(patient_id):
    appointments = Appointment.query.filter_by(patient_id=patient_id).all()

    result = []
    for a in appointments:
        treatment = Treatment.query.filter_by(appointment_id=a.id).first()
        result.append({
            "appointment_id": a.id,
            "date": str(a.date),
            "status": a.status,
            "diagnosis": treatment.diagnosis if treatment else None,
            "prescription": treatment.prescription if treatment else None,
            "notes": treatment.notes if treatment else None
        })

    return jsonify(result)
