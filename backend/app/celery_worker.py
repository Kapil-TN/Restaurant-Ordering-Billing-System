from app.celery_app import celery_app
from app.admin import tasks  # noqa: F401 — imported so tasks get registered
