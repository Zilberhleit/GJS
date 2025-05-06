import json
import uuid
from datetime import datetime, timedelta

from django.db.models.signals import post_init, pre_save
from django.test import TestCase
from django.urls import reverse
from jam_polls.models import *
from jams.models import GameJam
from jams.signals import *
from users.models import User


class PollViewTest(TestCase):
    def setUp(self):
        post_init.disconnect(post_init_previous_jam_status_handler, sender=GameJam)
        pre_save.disconnect(calculate_winner_when_jam_finished, sender=GameJam)
        pre_save.disconnect(set_final_theme_when_jam_prepared, sender=GameJam)
        pre_save.disconnect(set_random_themes_for_jam_when_it_created, sender=GameJam)

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.jam_case_1 = GameJam.objects.create(
            uuid=uuid.uuid4(),
            title="Summer Game Jam 2023",
            date_start=datetime.now(),
            date_end=(datetime.now() + timedelta(days=3)),
            theme="Space Exploration",
            status='PR'
        )
        self.question1 = GameJamTheme.objects.create(theme='Question 1', gamejam=self.jam_case_1)
        self.question2 = GameJamTheme.objects.create(theme='Question 2', gamejam=self.jam_case_1)
        self.url = reverse('poll', kwargs={'uuid': self.jam_case_1.uuid})

    def tearDown(self):
        post_init.connect(post_init_previous_jam_status_handler, sender=GameJam)
        pre_save.connect(calculate_winner_when_jam_finished, sender=GameJam)
        pre_save.connect(set_final_theme_when_jam_prepared, sender=GameJam)
        pre_save.connect(set_random_themes_for_jam_when_it_created, sender=GameJam)

    def test_poll_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/jam_polls_pages/poll.html')
        self.assertContains(response, GameJamTheme.objects.get(id=1).theme)

    def test_submit_poll(self):
        """Тестирование прохождения опроса"""
        response = self.client.post(reverse('submit', kwargs={'uuid': self.jam_case_1.uuid}),
                                    data=json.dumps({
                                        'result': [
                                            {'id': self.question1.id, 'decision': True},
                                            {'id': self.question2.id, 'decision': False}
                                        ]
                                    }),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "Все вопросы пройдены успешно")
        self.assertTrue(response.json()['redirect'])
        self.assertTrue(self.jam_case_1.users.filter(id=self.user.id).exists())

        self.question1.refresh_from_db()
        self.question2.refresh_from_db()
        self.assertTrue(ThemeVote.objects.filter(theme=self.question1, vote=True).exists())
        self.assertEqual(ThemeVote.objects.filter(theme=self.question1, vote=True).count(), 1)
        self.assertEqual(ThemeVote.objects.filter(theme=self.question2, vote=False).count(), 1)

        """Повторная попытка пройти тест"""
        response = self.client.post(reverse('submit', kwargs={'uuid': self.jam_case_1.uuid}),
                                    data=json.dumps({
                                        'result': [
                                            {'id': self.question1.id, 'decision': True},
                                            {'id': self.question2.id, 'decision': False}
                                        ]
                                    }),
                                    content_type='application/json')
        print('TSP response: ', response)
        print('TSP JSON response: ', response.json())
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['error'], 'Вы уже прошли опрос')
