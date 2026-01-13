from flask import Blueprint, request, jsonify, session
from datetime import datetime

from models import User, Patient, Doctor, Appointment, Treatment
from extensions import db
from utils.decorators import login_required

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
    user_id = session.get("user_id")

    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return jsonify({"error": "Patient profile not found"}), 404

    return jsonify({
        "patient_id": patient.id,
        "age": patient.age
    })

from models import Doctor, User

@patient_bp.route("/doctors", methods=["GET"])
@login_required(role="patient")
def list_doctors_for_patient():
    doctors = Doctor.query.all()

    result = []
    for d in doctors:
        user = User.query.get(d.user_id)
        result.append({
            "doctor_id": d.id,
            "name": user.name if user else None,
            "department_id": d.department_id,
            "is_available": d.is_available
        })

    return jsonify(result)


from datetime import datetime
from models import Appointment
from extensions import db

@patient_bp.route("/appointments", methods=["POST"])
@login_required(role="patient")
def book_appointment():
    data = request.get_json()
    user_id = session.get("user_id")

    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    doctor_id = data.get("doctor_id")
    date = datetime.strptime(data.get("date"), "%Y-%m-%d").date()
    time = datetime.strptime(data.get("time"), "%H:%M").time()

    # Prevent double booking
    existing = Appointment.query.filter_by(
        doctor_id=doctor_id,
        date=date,
        time=time,
        status="Booked"
    ).first()

    if existing:
        return jsonify({"error": "Doctor already booked for this slot"}), 400

    appointment = Appointment(
        patient_id=patient.id,
        doctor_id=doctor_id,
        date=date,
        time=time,
        status="Booked"
    )

    db.session.add(appointment)
    db.session.commit()

    return jsonify({
        "message": "Appointment booked successfully",
        "appointment_id": appointment.id
    })


@patient_bp.route("/appointments", methods=["GET"])
@login_required(role="patient")
def view_patient_appointments():
    user_id = session.get("user_id")
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


@patient_bp.route("/appointments/<int:appointment_id>/cancel", methods=["PUT"])
@login_required(role="patient")
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    appointment.status = "Cancelled"
    db.session.commit()

    return jsonify({"message": "Appointment cancelled"})

from models import Treatment

@patient_bp.route("/history", methods=["GET"])
@login_required(role="patient")
def patient_history():
    user_id = session.get("user_id")
    patient = Patient.query.filter_by(user_id=user_id).first()

    appointments = Appointment.query.filter_by(patient_id=patient.id).all()

    result = []
    for a in appointments:
        treatment = Treatment.query.filter_by(appointment_id=a.id).first()
        result.append({
            "appointment_id": a.id,
            "status": a.status,
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

    user_id = session.get("user_id")
    patient = Patient.query.filter_by(user_id=user_id).first()

    export_patient_treatments.delay(patient.id)

    return jsonify({"message": "Export started. You will be notified."})