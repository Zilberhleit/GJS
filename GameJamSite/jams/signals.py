import random

from django.contrib.auth import get_user_model
from django.db.models import Max, Count, Q
from django.db.models.signals import pre_save, post_init
from django.dispatch import receiver

from jam_polls.models import GameJamTheme, Theme
from jams.models import GameJam
from jams.views import count_jam_rating


@receiver(post_init, sender=GameJam)
def post_init_previous_jam_status_handler(sender, instance, **kwargs):
    """ Сигнал записывающий предыдущий статус геймджема (исползуется в других сигналах) """
    instance.previous_status = instance.status


@receiver(pre_save, sender=GameJam)
def calculate_winner_when_jam_finished(sender, instance, **kwargs):
    """ Сигнал вычисляющий победителя при завершении геймджема """
    if instance.previous_status != 'FN' and instance.status == 'FN':
        instance.previous_status = 'FN'

        final_rating = count_jam_rating(instance.uuid).order_by('-avg_rating')

        if final_rating.exists():
            winner_id = final_rating.first()['user__id']

            winner_user = get_user_model().objects.filter(id=winner_id)

            if winner_user.exists():
                instance.winner = winner_user[0]
                instance.save()



@receiver(pre_save, sender=GameJam)
def set_final_theme_when_jam_prepared(sender, instance, **kwargs):
    """ Сигнал устанавливающий тему окончания подготовки джема """
    if instance.previous_status == 'PR' and instance.status == 'OG':
        instance.previous_status = 'OG'

        jam_polls = GameJamTheme.objects.filter(gamejam=instance)

        themes_with_difference = jam_polls.annotate(
            true_votes=Count('themevote', filter=Q(themevote__vote=True)),
            false_votes=Count('themevote', filter=Q(themevote__vote=False)),
            difference=Count('themevote', filter=Q(themevote__vote=True)) - Count('themevote', filter=Q(themevote__vote=False))
        )

        theme_with_max_difference = themes_with_difference.order_by('-difference').first()

        if theme_with_max_difference:
            instance.theme = theme_with_max_difference.theme
        else:
            instance.theme = None


@receiver(pre_save, sender=GameJam)
def set_random_themes_for_jam_when_it_created(sender, instance, **kwargs):
    """ Сигнал выбирающий 3-и случайные темы на голосование при создании геймджема """
    if instance.status == 'PR' and not GameJamTheme.objects.filter(gamejam=instance).exists():
        themes_max_pk = Theme.objects.all().aggregate(Max('pk'))['pk__max']

        random_picked_themes = Theme.objects.filter(pk__in=random.sample(range(1, themes_max_pk + 1), 3))
        GameJamTheme.objects.bulk_create([GameJamTheme(gamejam=instance, theme=theme)
                                          for theme in random_picked_themes])



