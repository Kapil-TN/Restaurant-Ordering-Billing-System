from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    'restaurant_admin',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)

celery_app.conf.update(
    timezone='Asia/Kolkata',
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    'monthly-admin-report': {
        'task': 'admin.send_monthly_report',
        'schedule': crontab(day_of_month=1, hour=9, minute=0),
    },
    'daily-reengagement-check': {
        'task': 'admin.send_reengagement_emails',
        'schedule': crontab(hour=9, minute=0),
    },
}
