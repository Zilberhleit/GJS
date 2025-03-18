from django.contrib.auth import get_user_model
from django.db.models import Max
from django.db.models.signals import pre_save, post_init
from django.dispatch import receiver

from jam_polls.models import Poll
from jams.models import GameJam
from jams.views import count_final_rating


@receiver(post_init, sender=GameJam)
def post_init_previous_jam_status_handler(sender, instance, **kwargs):
    instance.previous_status = instance.status


# Сигнал вычисляющий победителя при завершении геймджема

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


# Сигнал устанавливающий тему окончания подготовки джема

@receiver(pre_save, sender=GameJam)
def set_final_theme_when_jam_prepared(sender, instance, **kwargs):
    if instance.previous_status == 'PR' and instance.status == 'OG':
        instance.previous_status = 'OG'

        jam_polls = Poll.objects.filter(jam_uuid=instance.uuid)

        theme = jam_polls.filter(total_votes=jam_polls.aggregate(Max('count'))['count__max']).first()

        instance.theme =theme.question_text
