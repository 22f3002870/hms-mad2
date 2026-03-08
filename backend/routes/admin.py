from flask import Blueprint, request, jsonify
from utils.decorators import login_required
from models import Doctor, Patient, Appointment, User, Department, Treatment
from extensions import db, redis_client
import json

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

# ---------------------------------------------------
# ADMIN DASHBOARD
# ---------------------------------------------------
@admin_bp.route("/dashboard", methods=["GET"])
@login_required(role="admin")
def admin_dashboard():
    cache_key = "admin:dashboard"

    try:
        cached = redis_client.get(cache_key)
        if cached:
            return jsonify(json.loads(cached))
    except Exception as e:
        print("⚠️ Redis error:", e)

    data = {
        "total_doctors": Doctor.query.count(),
        "total_patients": Patient.query.count(),
        "total_appointments": Appointment.query.count()
    }

    try:
        redis_client.setex(cache_key, 120, json.dumps(data))
    except Exception as e:
        print("⚠️ Redis set error:", e)

    return jsonify(data)


# ---------------------------------------------------
# DOCTORS
# ---------------------------------------------------
@admin_bp.route("/doctors", methods=["POST"])
@login_required(role="admin")
def create_doctor():
    data = request.json

    required = ["name", "email", "password", "department_id"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Doctor already exists"}), 400

    user = User(
        name=data["name"],
        email=data["email"],
        role="doctor",
        is_active=True
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    doctor = Doctor(
        user_id=user.id,
        department_id=data["department_id"],
        is_available=True
    )
    db.session.add(doctor)
    db.session.commit()

    return jsonify({"message": "Doctor created successfully"})


@admin_bp.route("/doctors", methods=["GET"])
@login_required(role="admin")
def list_doctors():
    doctors = Doctor.query.all()

    return jsonify([
        {
            "doctor_id": d.id,
            "name": d.user.name,
            "email": d.user.email,
            "department": d.department.name if d.department else None,
            "department_id": d.department_id,
            "is_available": d.is_available
        }
        for d in doctors
    ])


# ---------------------------------------------------
# PATIENTS
# ---------------------------------------------------
@admin_bp.route("/patients", methods=["GET"])
@login_required(role="admin")
def list_patients():
    patients = Patient.query.all()

    return jsonify([
        {
            "patient_id": p.id,
            "name": p.user.name,
            "email": p.user.email,
            "age": p.age
        }
        for p in patients
    ])



# ---------------------------------------------------
# APPOINTMENTS
# ---------------------------------------------------
from sqlalchemy.orm import joinedload
from models import Appointment, Doctor, Patient, Treatment

@admin_bp.route("/appointments", methods=["GET"])
@login_required(role="admin")
def view_appointments():
    appointments = (
        Appointment.query
        .options(
            joinedload(Appointment.doctor).joinedload(Doctor.user),
            joinedload(Appointment.doctor).joinedload(Doctor.department),
            joinedload(Appointment.patient).joinedload(Patient.user),
            joinedload(Appointment.treatment) 
        )
        .order_by(Appointment.date.desc(), Appointment.time.desc())
        .all()
    )

    result = []

    for a in appointments:
        treatment = Treatment.query.filter_by(
            appointment_id=a.id
        ).first()

        result.append({
            # 🧾 Appointment
            "appointment_id": a.id,
            "date": str(a.date),
            "time": str(a.time),
            "status": a.status,

            # 👨‍⚕️ Doctor
            "doctor_id": a.doctor.id if a.doctor else None,
            "doctor_name": a.doctor.user.name if a.doctor and a.doctor.user else None,

            # 🏥 Department
            "department_id": a.doctor.department.id if a.doctor and a.doctor.department else None,
            "department_name": (
                a.doctor.department.name
                if a.doctor and a.doctor.department
                else "—"
            ),

            # 🧑‍🦱 Patient
            "patient_id": a.patient.id if a.patient else None,
            "patient_name": a.patient.user.name if a.patient and a.patient.user else None,

            # 💊 Treatment (read-only)
            "has_treatment": treatment is not None,
            "diagnosis": treatment.diagnosis if treatment else None,
            "prescription": treatment.prescription if treatment else None,
            "notes": treatment.notes if treatment else None
        })

    return jsonify(result)






# ---------------------------------------------------
# DEPARTMENTS
# ---------------------------------------------------
@admin_bp.route("/departments", methods=["GET"])
@login_required(role="admin")
def list_departments():
    departments = Department.query.all()

    return jsonify([
        {
            "id": d.id,
            "name": d.name,
            "description": d.description
        }
        for d in departments
    ])


@admin_bp.route("/departments", methods=["POST"])
@login_required(role="admin")
def create_department():
    data = request.json

    name = data.get("name")
    description = data.get("description", "")

    if not name:
        return jsonify({"error": "Department name is required"}), 400

    if Department.query.filter_by(name=name).first():
        return jsonify({"error": "Department already exists"}), 400

    department = Department(
        name=name,
        description=description
    )
    db.session.add(department)
    db.session.commit()

    return jsonify({"message": "Department created successfully"})
