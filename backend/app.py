print("app.py file is executing")

from flask import Flask
from config import Config
from extensions import db

from routes.auth import auth_bp
from routes.patient import patient_bp
from routes.admin import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(patient_bp, url_prefix="/api/patient")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    return app



app = create_app()
if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host="127.0.0.1", port=5000, debug=True)
