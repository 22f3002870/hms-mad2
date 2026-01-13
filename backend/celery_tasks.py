from celery_worker import celery
from datetime import date
import csv

from app import create_app
from models import Appointment, Patient, User, Doctor, Treatment


def with_app_context(fn):
    """
    Helper decorator to ensure Flask app context
    inside Celery tasks
    """
    def wrapper(*args, **kwargs):
        app = create_app()
        with app.app_context():
            return fn(*args, **kwargs)
    return wrapper


@celery.task
@with_app_context
def daily_appointment_reminder():
    today = date.today()

    appointments = Appointment.query.filter_by(
        date=today,
        status="Booked"
    ).all()

    for appt in appointments:
        patient = Patient.query.get(appt.patient_id)
        user = User.query.get(patient.user_id)

        print(
            f"[REMINDER] Patient {user.email} "
            f"has appointment today at {appt.time}"
        )


@celery.task
@with_app_context
def monthly_doctor_report():
    doctors = Doctor.query.all()

    for doctor in doctors:
        appointments = Appointment.query.filter_by(
            doctor_id=doctor.id,
            status="Completed"
        ).all()

        print(
            f"[MONTHLY REPORT] Doctor {doctor.id} "
            f"handled {len(appointments)} appointments"
        )


@celery.task
@with_app_context
def export_patient_treatments(patient_id):
    patient = Patient.query.get(patient_id)
    user = User.query.get(patient.user_id)

    filename = f"patient_{patient_id}_treatments.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Date",
            "Doctor ID",
            "Diagnosis",
            "Prescription"
        ])

        appointments = Appointment.query.filter_by(
            patient_id=patient_id,
            status="Completed"
        ).all()

        for appt in appointments:
            treatment = Treatment.query.filter_by(
                appointment_id=appt.id
            ).first()

            if treatment:
                writer.writerow([
                    appt.date,
                    appt.doctor_id,
                    treatment.diagnosis,
                    treatment.prescription
                ])

    print(f"[CSV EXPORT DONE] {filename}")
