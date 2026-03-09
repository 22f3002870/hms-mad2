from flask import Blueprint, jsonify, request
from utils.decorators import login_required
from extensions import db, redis_client
from models import Doctor, Appointment, Treatment
import json

doctor_bp = Blueprint("doctor", __name__)

# ---------------------------------------------------
# 1️⃣ DOCTOR DASHBOARD (SUMMARY)
# ---------------------------------------------------
@doctor_bp.route("/dashboard", methods=["GET"])
@login_required(role="doctor")
def doctor_dashboard():
    user_id = request.user_id


    doctor = Doctor.query.filter_by(user_id=user_id).first()
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    cache_key = f"doctor:dashboard:{doctor.id}"
    cached = redis_client.get(cache_key)
    if cached:
        return jsonify(json.loads(cached))

    data = {
        "total_appointments": Appointment.query.filter_by(
            doctor_id=doctor.id
        ).count(),
        "completed": Appointment.query.filter_by(
            doctor_id=doctor.id, status="Completed"
        ).count(),
        "pending": Appointment.query.filter_by(
            doctor_id=doctor.id, status="Booked"
        ).count(),
    }

    redis_client.setex(cache_key, 60, json.dumps(data))
    return jsonify(data)


# ---------------------------------------------------
# 2️⃣ LIST DOCTOR APPOINTMENTS
# ---------------------------------------------------
@doctor_bp.route("/appointments", methods=["GET"])
@login_required(role="doctor")
def get_doctor_appointments():
    user_id = request.user_id

    doctor = Doctor.query.filter_by(user_id=user_id).first()

    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    appointments = Appointment.query.filter_by(
        doctor_id=doctor.id
    ).all()

    return jsonify([
        {
            "appointment_id": a.id,
            "date": str(a.date),
            "time": str(a.time),
            "status": a.status,
            "patient_name": a.patient.user.name,
            "patient_id": a.patient.id,
            "has_treatment": Treatment.query.filter_by(
                appointment_id=a.id
            ).first() is not None

        }
        for a in appointments
    ])


# ---------------------------------------------------
# 3️⃣ COMPLETE APPOINTMENT + ADD TREATMENT
# ---------------------------------------------------
@doctor_bp.route("/appointments/<int:appointment_id>/treatment", methods=["POST"])
@login_required(role="doctor")
def add_treatment(appointment_id):
    data = request.get_json()
    user_id = request.user_id


    doctor = Doctor.query.filter_by(user_id=user_id).first()
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    appointment = Appointment.query.get_or_404(appointment_id)

    if appointment.doctor_id != doctor.id:
        return jsonify({"error": "Unauthorized"}), 403

    if appointment.status != "Booked":
        return jsonify({"error": "Appointment already processed"}), 400

    if Treatment.query.filter_by(
        appointment_id=appointment.id
    ).first():
        return jsonify({"error": "Treatment already exists"}), 400

    treatment = Treatment(
        appointment_id=appointment.id,
        diagnosis=data.get("diagnosis"),
        prescription=data.get("prescription"),
        notes=data.get("notes")
    )

    appointment.status = "Completed"
    db.session.add(treatment)
    db.session.commit()

    # ✅ Clear dashboard cache
    redis_client.delete(f"doctor:dashboard:{doctor.id}")

    return jsonify({
        "message": "Appointment completed & treatment added"
    })


# ---------------------------------------------------
# 4️⃣ VIEW PATIENT HISTORY (DOCTOR-SPECIFIC)
# ---------------------------------------------------
@doctor_bp.route("/patients/<int:patient_id>/history", methods=["GET"])
@login_required(role="doctor")
def patient_history(patient_id):
    user_id = request.user_id   # ✅ FIXED

    doctor = Doctor.query.filter_by(user_id=user_id).first()
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    appointments = (
        Appointment.query
        .filter_by(doctor_id=doctor.id, patient_id=patient_id)
        .all()
    )

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



@doctor_bp.route("/appointments/<int:appointment_id>/treatment", methods=["PUT"])
@login_required(role="doctor")
def update_treatment(appointment_id):
    data = request.get_json()
    user_id = request.user_id

    doctor = Doctor.query.filter_by(user_id=user_id).first()
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    appointment = Appointment.query.get_or_404(appointment_id)

    if appointment.doctor_id != doctor.id:
        return jsonify({"error": "Unauthorized"}), 403

    if not appointment.treatment:
        return jsonify({"error": "Treatment not found"}), 404

    # ✅ UPDATE FIELDS
    appointment.treatment.diagnosis = data.get("diagnosis")
    appointment.treatment.prescription = data.get("prescription")
    appointment.treatment.notes = data.get("notes")

    db.session.commit()

    return jsonify({"message": "Treatment updated successfully"})



@doctor_bp.route("/appointments/<int:appointment_id>/treatment", methods=["GET"])
@login_required(role="doctor")
def get_treatment(appointment_id):
    user_id = request.user_id

    doctor = Doctor.query.filter_by(user_id=user_id).first()
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    appointment = Appointment.query.get_or_404(appointment_id)

    if appointment.doctor_id != doctor.id:
        return jsonify({"error": "Unauthorized"}), 403

    treatment = Treatment.query.filter_by(
        appointment_id=appointment.id
    ).first()

    if not treatment:
        return jsonify({"error": "No treatment found"}), 404

    return jsonify({
        "diagnosis": treatment.diagnosis,
        "prescription": treatment.prescription,
        "notes": treatment.notes
    })


# ---------------- CANCEL APPOINTMENT ----------------
@doctor_bp.route("/appointments/<int:appointment_id>/cancel", methods=["PUT"])
@login_required(role="doctor")
def cancel_appointment(appointment_id):

    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    if appointment.status != "Booked":
        return jsonify({
            "error": "Only booked appointments can be cancelled"
        }), 400

    appointment.status = "Cancelled"

    db.session.commit()

    # Invalidate cache
    redis_client.delete(f"doctor:dashboard:{appointment.doctor_id}")

    return jsonify({
        "message": "Appointment cancelled successfully"
    })

# ---------------- UPDATE AVAILABILITY ----------------
@doctor_bp.route("/availability", methods=["PUT"])
@login_required(role="doctor")
def update_availability():

    user_id = request.user_id
    data = request.json

    doctor = Doctor.query.filter_by(user_id=user_id).first()

    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    doctor.is_available = data.get("is_available", True)

    db.session.commit()

    return jsonify({
        "message": "Availability updated",
        "is_available": doctor.is_available
    })