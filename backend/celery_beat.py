from celery.schedules import crontab
from celery_worker import celery

celery.conf.beat_schedule = {
    "daily-reminder-job": {
        "task": "celery_tasks.daily_appointment_reminder",
        "schedule": crontab(hour=9, minute=0),  # every day at 9 AM
    }
}

celery.conf.beat_schedule.update({
    "monthly-doctor-report": {
        "task": "celery_tasks.monthly_doctor_report",
        "schedule": crontab(day_of_month=1, hour=10, minute=0),
    }
})
