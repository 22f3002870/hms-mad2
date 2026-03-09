from celery_worker import celery
from datetime import date
import csv
import requests
from functools import wraps
from app import create_app
from models import Appointment, Patient, User, Doctor, Treatment


# --------------------------------------------------
# GOOGLE CHAT WEBHOOK
# --------------------------------------------------

WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAQAiwMkmHE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=m9GYj99z0UUgKQ9Pe-qayc-7eKqvYQOn1PJPlDX4X9E"


# --------------------------------------------------
# APP CONTEXT WRAPPER
# --------------------------------------------------

def with_app_context(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        app = create_app()
        with app.app_context():
            return fn(*args, **kwargs)
    return wrapper


# --------------------------------------------------
# DAILY APPOINTMENT REMINDER
# --------------------------------------------------

@celery.task
@with_app_context
def daily_appointment_reminder():

    today = date.today()

    appointments = Appointment.query.filter_by(
        date=str(today),
        status="Booked"
    ).all()

    if not appointments:
        print("[REMINDER JOB] No appointments today")
        return

    for appt in appointments:

        patient = Patient.query.get(appt.patient_id)
        user = User.query.get(patient.user_id)

        message = (
            f"Reminder: {user.name}, you have an appointment today "
            f"at {appt.time}. Please visit the hospital."
        )

        # Send notification to Google Chat
        try:
            requests.post(
                WEBHOOK_URL,
                json={"text": message}
            )
            print("[DAILY REMINDER SENT]", message)

        except Exception as e:
            print("[REMINDER ERROR]", str(e))


# --------------------------------------------------
# MONTHLY DOCTOR ACTIVITY REPORT
# --------------------------------------------------

@celery.task
@with_app_context
def monthly_doctor_report():

    doctors = Doctor.query.all()

    for doctor in doctors:

        appointments = Appointment.query.filter_by(
            doctor_id=doctor.id,
            status="Completed"
        ).all()

        if not appointments:
            continue

        report = f"<b>Monthly Activity Report</b>\nDoctor ID: {doctor.id}\n\n"

        for appt in appointments:

            treatment = Treatment.query.filter_by(
                appointment_id=appt.id
            ).first()

            diagnosis = treatment.diagnosis if treatment else "N/A"
            prescription = treatment.prescription if treatment else "N/A"

            report += (
                f"Date: {appt.date}\n"
                f"Diagnosis: {diagnosis}\n"
                f"Prescription: {prescription}\n\n"
            )

        try:
            requests.post(
                WEBHOOK_URL,
                json={"text": report}
            )

            print("[MONTHLY REPORT SENT]")
            print(report)

        except Exception as e:
            print("[REPORT ERROR]", str(e))


# --------------------------------------------------
# USER TRIGGERED CSV EXPORT
# --------------------------------------------------

@celery.task
@with_app_context
def export_patient_treatments(patient_id):

    patient = Patient.query.get(patient_id)
    user = User.query.get(patient.user_id)

    filename = f"exports/patient_{patient_id}_treatments.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Appointment Date",
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

    message = (
        f"CSV Export Completed for {user.name}\n"
        f"File Generated: {filename}"
    )

    try:

        requests.post(
            WEBHOOK_URL,
            json={"text": message}
        )

        print("[CSV EXPORT COMPLETE]", filename)

    except Exception as e:

        print("[CSV WEBHOOK ERROR]", str(e))