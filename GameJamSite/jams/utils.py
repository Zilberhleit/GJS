import json
import random
from datetime import datetime, timedelta
from time import time, timezone

from django.db.models import DateTimeField
from django.utils import timezone
from django_celery_beat.models import ClockedSchedule, PeriodicTask


def rand_date():
    """Функция генерирующая случайную дату в некотором промежутке"""
    start = datetime.now()
    end = start + timedelta(days=3)
    return start + (end - start) * random.random()


def create_gamejam_change_status_periodic_task(
    gamejam_instance, new_status: str, run_at: DateTimeField
):
    """Создает периодическую задачу для изменения статуса геймджема"""

    clocked, _ = ClockedSchedule.objects.get_or_create(clocked_time=run_at)

    kwargs = {"new_status": new_status, "gamejam_uuid": str(gamejam_instance.uuid)}
    task_name = f"Update gamejam status {gamejam_instance.title} to {new_status}"

    PeriodicTask.objects.update_or_create(
        name=task_name,
        defaults={
            "task": "jams.tasks.change_gamejam_status",
            "kwargs": json.dumps(kwargs),
            "clocked": clocked,
            "one_off": True,
            "enabled": True,
        },
    )


def update_gamejam_change_status_periodic_task(
    gamejam_instance, new_status: str, run_at: DateTimeField
):
    """Обновляет периодические задачи для изменения статуса геймджема"""
    old_task_name = f"Update gamejam status {gamejam_instance.title} to {new_status}"
    PeriodicTask.objects.filter(name=old_task_name).delete()

    if run_at and run_at > timezone.now():
        create_gamejam_change_status_periodic_task(gamejam_instance, new_status, run_at)
