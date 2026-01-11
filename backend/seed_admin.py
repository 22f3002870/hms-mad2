from app import app
from models import User
from extensions import db

with app.app_context():
    admin = User.query.filter_by(role="admin").first()

    if not admin:
        admin = User(
            name="Admin",
            email="admin@hospital.com",
            role="admin"
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()

        print("Admin created")
