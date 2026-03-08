class Config:
    SECRET_KEY = "secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///hms.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    broker_url = "redis://localhost:6379/0"
    result_backend = "redis://localhost:6379/0"

    # 🔑 SESSION FIXES
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = False
