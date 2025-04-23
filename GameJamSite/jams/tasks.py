
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from jams.models import GameJam


@shared_task(bind=True, autoretry_for=(ObjectDoesNotExist,), retry_kwargs={'max_retries': 3, 'countdown': 5})
def change_gamejam_status(self, new_status : str, gamejam_uuid : str):
    gamejam = GameJam.objects.get(uuid=gamejam_uuid)
    gamejam.status = new_status
    gamejam.save()