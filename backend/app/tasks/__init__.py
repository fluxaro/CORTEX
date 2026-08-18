"""Celery tasks package."""

from app.tasks.analysis_tasks import static_analysis_task
from app.tasks.architecture_tasks import architecture_analysis_task
from app.tasks.enterprise_tasks import (
    notification_dispatch_task,
    repository_sync_task,
    scheduled_scan_task,
    trend_generation_task,
    webhook_processing_task,
)
from app.tasks.repository_grading_tasks import (
    repository_grading_task,
    repository_iq_task,
)
from app.tasks.repository_intelligence_tasks import repository_intelligence_task
from app.tasks.repository_tasks import clone_repository_task
from app.tasks.security_tasks import security_analysis_task

__all__ = [
    "clone_repository_task",
    "static_analysis_task",
    "architecture_analysis_task",
    "security_analysis_task",
    "repository_intelligence_task",
    "repository_grading_task",
    "repository_iq_task",
    "repository_sync_task",
    "scheduled_scan_task",
    "trend_generation_task",
    "webhook_processing_task",
    "notification_dispatch_task",
]
