from flask import Flask
from extensions import db
from flask_cors import CORS

from routes.admin import admin_bp
from routes.doctor import doctor_bp
from routes.auth import auth_bp
from routes.patient import patient_bp

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dev-secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hms.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    CORS(app, supports_credentials=True)

    db.init_app(app)

    # ROUTES
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(doctor_bp, url_prefix="/api/doctor")
    app.register_blueprint(patient_bp, url_prefix="/api/patient")

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)