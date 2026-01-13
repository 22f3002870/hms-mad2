from celery import Celery
from config import Config

celery = Celery(
    "hms",
    broker=Config.broker_url,
    backend=Config.result_backend
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True
)
