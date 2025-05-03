import json
from datetime import datetime, timedelta
import random

from django.db.models import DateTimeField
from django_celery_beat.models import PeriodicTask, ClockedSchedule



def rand_date():
    """ Функция генерирующая случайную дату в некотором промежутке """
    start = datetime.now()
    end = start + timedelta(days=3)
    return start + (end - start) * random.random()



def create_gamejam_change_status_periodic_task(gamejam_instance ,
                                               new_status: str,
                                               run_at: DateTimeField):
    """ Создает периодическую задачу для изменения статуса геймджема """

    clocked, _ = ClockedSchedule.objects.get_or_create(
        clocked_time=run_at
    )

    kwargs = {'new_status': new_status, 'gamejam_uuid': str(gamejam_instance.uuid)}
    task_name = f'Update gamejam status {gamejam_instance.title} to {new_status}'

    PeriodicTask.objects.update_or_create(
        name=task_name,
        defaults={
            'task': 'jams.tasks.change_gamejam_status',
            'kwargs': json.dumps(kwargs),
            'clocked': clocked,
            'one_off': True
        }
    )