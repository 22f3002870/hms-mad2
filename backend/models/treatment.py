from extensions import db
from datetime import datetime

class Treatment(db.Model):
    __tablename__ = "treatments"

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(
        db.Integer,
        db.ForeignKey("appointments.id"),
        unique=True
    )

    appointment = db.relationship(
        "Appointment",
        back_populates="treatment"
    )
