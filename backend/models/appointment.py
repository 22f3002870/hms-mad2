from extensions import db
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    status = db.Column(db.String(20), default="Booked")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
