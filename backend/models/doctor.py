from extensions import db

class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    is_available = db.Column(db.Boolean, default=True)

    user = db.relationship("User", back_populates="doctor")
    department = db.relationship("Department", back_populates="doctors")
    appointments = db.relationship("Appointment", back_populates="doctor")