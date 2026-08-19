"""Celery task queue initialization."""

from celery import Celery

from app.core.config.settings import settings

celery_app = Celery(
    "cortex_workers",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.analysis_tasks",
        "app.tasks.architecture_tasks",
        "app.tasks.enterprise_tasks",
        "app.tasks.repository_grading_tasks",
        "app.tasks.repository_intelligence_tasks",
        "app.tasks.repository_tasks",
        "app.tasks.security_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)
