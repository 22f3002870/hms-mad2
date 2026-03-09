from flask import Blueprint, request, jsonify
from datetime import datetime

from models import User, Patient, Doctor, Appointment, Treatment
from extensions import db
from utils.decorators import login_required

from extensions import redis_client

patient_bp = Blueprint("patient", __name__)


@patient_bp.route("/register", methods=["POST"])
def register_patient():
    data = request.get_json()

    # 1. Basic validation
    if not data or not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({
            "error": "Name, email and password are required"
        }), 400

    # 2. Check email uniqueness
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({
            "error": "Email already registered"
        }), 400

    try:
        # 3. Create user
        user = User(
            name=data["name"],
            email=data["email"],
            role="patient"
        )
        user.set_password(data["password"])
        db.session.add(user)
        db.session.flush()  # get user.id without commit

        # 4. Create patient profile
        patient = Patient(
            user_id=user.id,
            age=data.get("age")
        )
        db.session.add(patient)

        # 5. Commit once (atomic transaction)
        db.session.commit()

        return jsonify({
            "message": "Patient registered successfully",
            "patient_id": patient.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Registration failed",
            "details": str(e)
        }), 500


from flask import session
from utils.decorators import login_required
from models import Patient

@patient_bp.route("/dashboard", methods=["GET"])
@login_required(role="patient")
def patient_dashboard():
    user_id = request.user_id


    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return jsonify({"error": "Patient profile not found"}), 404

    return jsonify({
        "patient_id": patient.id,
        "age": patient.age
    })

from models import Doctor, User

from extensions import redis_client
import json

@patient_bp.route("/doctors", methods=["GET"])
@login_required(role="patient")
def list_doctors_for_patient():
    cache_key = "patient:doctors"

    # 1️⃣ Try Redis cache
    cached = redis_client.get(cache_key)
    if cached:
        return jsonify(json.loads(cached))

    # 2️⃣ DB fallback
    doctors = Doctor.query.filter_by(is_available=True).all()
    result = []

    for d in doctors:
        result.append({
            "doctor_id": d.id,
            "doctor_name": d.user.name,
            "department_name": d.department.name if d.department else None,
            "department_description": d.department.description if d.department else None,
            "is_available": d.is_available
        })

    # 3️⃣ Save to Redis (TTL = 60s)
    redis_client.setex(cache_key, 60, json.dumps(result))

    return jsonify(result)

from datetime import datetime
from models import Appointment
from extensions import db

@patient_bp.route("/appointments", methods=["POST"])
@login_required(role="patient")
def book_appointment():
    data = request.get_json()
    user_id = request.user_id

    # Validate request body
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    doctor_id = data.get("doctor_id")
    date_str = data.get("date")
    time_str = data.get("time")

    # Validate required fields
    if not doctor_id or not date_str or not time_str:
        return jsonify({
            "error": "doctor_id, date and time are required"
        }), 400

    # Convert date/time safely
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        time = datetime.strptime(time_str, "%H:%M").strftime("%H:%M")
    except ValueError:
        return jsonify({
            "error": "Invalid date or time format"
        }), 400

    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    # Prevent double booking
    existing = Appointment.query.filter_by(
        doctor_id=doctor_id,
        date=date,
        time=time,
        status="Booked"
    ).first()

    if existing:
        return jsonify({
            "error": "Doctor already booked for this slot"
        }), 400

    # Create appointment
    appointment = Appointment(
        patient_id=patient.id,
        doctor_id=doctor_id,
        date=date,
        time=time,
        status="Booked"
    )

    db.session.add(appointment)
    db.session.commit()

    # Invalidate cache
    redis_client.delete("patient:doctors")
    redis_client.delete(f"doctor:dashboard:{doctor_id}")

    return jsonify({
        "message": "Appointment booked successfully",
        "appointment_id": appointment.id
    })


@patient_bp.route("/appointments", methods=["GET"])
@login_required(role="patient")
def view_patient_appointments():
    user_id = request.user_id

    patient = Patient.query.filter_by(user_id=user_id).first()

    appointments = Appointment.query.filter_by(patient_id=patient.id).all()

    result = []
    for a in appointments:
        result.append({
            "appointment_id": a.id,
            "doctor_id": a.doctor_id,
            "date": str(a.date),
            "time": str(a.time),
            "status": a.status
        })

    return jsonify(result)




from models import Treatment

@patient_bp.route("/history", methods=["GET"])
@login_required(role="patient")
def patient_history():

    user_id = request.user_id

    patient = Patient.query.filter_by(user_id=user_id).first()

    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    appointments = Appointment.query.filter_by(
        patient_id=patient.id
    ).order_by(Appointment.date.desc()).all()

    result = []

    for a in appointments:

        treatment = Treatment.query.filter_by(
            appointment_id=a.id
        ).first()

        result.append({
            "appointment_id": a.id,
            "status": a.status,

            # ADD THESE TWO
            "date": str(a.date) if a.date else None,
            "time": str(a.time) if a.time else None,

            "diagnosis": treatment.diagnosis if treatment else None,
            "prescription": treatment.prescription if treatment else None,
            "notes": treatment.notes if treatment else None
        })

    return jsonify(result)




# ---------------- EXPORT (CELERY) ----------------
@patient_bp.route("/export", methods=["POST"])
@login_required(role="patient")
def export_csv():
    from celery_tasks import export_patient_treatments  # ✅ IMPORT INSIDE FUNCTION

    user_id = request.user_id

    patient = Patient.query.filter_by(user_id=user_id).first()

    export_patient_treatments.delay(patient.id)

    return jsonify({"message": "Export started. You will be notified."})

from flask import send_file
import os


# ---------------- DOWNLOAD CSV ----------------
@patient_bp.route("/export/download", methods=["GET"])
@login_required(role="patient")
def download_csv():

    user_id = request.user_id

    patient = Patient.query.filter_by(user_id=user_id).first()

    filepath = f"exports/patient_{patient.id}_treatments.csv"

    if not os.path.exists(filepath):
        return jsonify({"error": "CSV not ready yet"}), 404

    return send_file(
        filepath,
        as_attachment=True
    )

# ---------------- CANCEL APPOINTMENT ----------------
@patient_bp.route("/appointments/<int:appointment_id>/cancel", methods=["PUT"])
@login_required(role="patient")
def cancel_appointment(appointment_id):

    user_id = request.user_id

    patient = Patient.query.filter_by(user_id=user_id).first()

    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    appointment = Appointment.query.filter_by(
        id=appointment_id,
        patient_id=patient.id
    ).first()

    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    if appointment.status != "Booked":
        return jsonify({"error": "Only booked appointments can be cancelled"}), 400

    appointment.status = "Cancelled"
    db.session.commit()

    # Invalidate doctor dashboard cache


    try:
        redis_client.delete(f"doctor:dashboard:{appointment.doctor_id}")
    except Exception:
        pass

    return jsonify({"message": "Appointment cancelled successfully"})

# ---------------- PATIENT PROFILE ----------------
@patient_bp.route("/profile", methods=["GET"])
@login_required(role="patient")
def get_profile():

    user_id = request.user_id

    patient = Patient.query.filter_by(user_id=user_id).first()

    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify({
        "name": patient.user.name,
        "email": patient.user.email,
        "age": patient.age
    })


# ---------------- UPDATE PROFILE ----------------
@patient_bp.route("/profile", methods=["PUT"])
@login_required(role="patient")
def update_profile():

    user_id = request.user_id
    data = request.json

    patient = Patient.query.filter_by(user_id=user_id).first()

    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    name = data.get("name")
    age = data.get("age")

    if name:
        patient.user.name = name

    if age:
        patient.age = age

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully"
    })

# ---------------- RESCHEDULE APPOINTMENT ----------------
@patient_bp.route("/appointments/<int:appointment_id>/reschedule", methods=["PUT"])
@login_required(role="patient")
def reschedule_appointment(appointment_id):

    data = request.get_json()
    date = data.get("date")
    time = data.get("time")

    if not date or not time:
        return jsonify({"error": "Date and time required"}), 400

    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    if appointment.status != "Booked":
        return jsonify({"error": "Only booked appointments can be rescheduled"}), 400

    # Prevent double booking
    existing = Appointment.query.filter_by(
        doctor_id=appointment.doctor_id,
        date=date,
        time=time,
        status="Booked"
    ).first()

    if existing:
        return jsonify({"error": "Doctor already booked for this slot"}), 400

    appointment.date = date
    appointment.time = time

    db.session.commit()

    return jsonify({
        "message": "Appointment rescheduled successfully"
    })