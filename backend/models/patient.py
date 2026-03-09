from extensions import db

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    age = db.Column(db.Integer)

    user = db.relationship("User", back_populates="patient")
    appointments = db.relationship("Appointment", back_populates="patient")