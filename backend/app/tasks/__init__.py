"""Background Celery tasks package."""

from app.tasks.analysis_tasks import static_analysis_task
from app.tasks.repository_tasks import clone_repository_task, prepare_analysis_task

__all__ = [
    "clone_repository_task",
    "prepare_analysis_task",
    "static_analysis_task",
]
