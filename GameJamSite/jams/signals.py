from django.contrib.auth import get_user_model
from django.dispatch import receiver

from jams.models import GameJam
from jams.views import count_final_rating
from django.db.models.signals import pre_save, post_init


@receiver(post_init, sender=GameJam)
def post_init_previous_jam_status_handler(sender, instance, **kwargs):
    instance.previous_status = instance.status

@receiver(pre_save, sender=GameJam)
def calculate_winner_when_jam_finished(sender, instance, **kwargs):
    if instance.previous_status != 'FN' and instance.status == 'FN':
        instance.previous_status = 'FN'

        final_rating = count_final_rating(instance.uuid).order_by('-avg_rating')

        if final_rating.exists():
            winner_id = final_rating.first()['user__id']

            winner_user = get_user_model().objects.filter(id=winner_id)

            if winner_user.exists():
                instance.winner = winner_user[0]
                instance.save()

