import uuid
from datetime import datetime, timedelta
from unittest import skip
import sys

from celery.utils.dispatch import signal
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.signals import post_init
from django.shortcuts import redirect
from django.test import TestCase
from django.urls import reverse
from jams.models import GameJam, Game, RatingUserJam
from jams.signals import *
from jams.views import count_final_rating
from users.models import User

class JamsViewTest(TestCase):
    """ Функция установки данных """
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
            status='OG'
        )
        self.jam_case_2 = GameJam.objects.create(
            uuid=uuid.uuid4(),
            title="Summer Game Jam 2024",
            date_start=datetime.now(),
            date_end=(datetime.now() + timedelta(days=3)),
            theme="Exploration",
            status='PR'
        )
        self.jam_case_1.users.set([self.user])
        self.jam_case_3 = GameJam.objects.create(
            uuid=uuid.uuid4(),
            title="Autumn Game Jam 2024",
            date_start=datetime.now(),
            date_end=(datetime.now() + timedelta(days=3)),
            theme="Exploration",
            status='OG'
        )
        self.user2, _ = User.objects.get_or_create(
            username='user2',
            email='user2@example.com',
            defaults={'password': 'testpassword2'}
        )
        self.jam_case_3.users.set([self.user, self.user2])
        RatingUserJam.objects.create(jam_uuid=self.jam_case_3, user=self.user, user_who_rate=self.user2, stars=4)
        RatingUserJam.objects.create(jam_uuid=self.jam_case_3, user=self.user2, user_who_rate=self.user, stars=3)

    def tearDown(self):
        post_init.connect(post_init_previous_jam_status_handler, sender=GameJam)
        pre_save.connect(calculate_winner_when_jam_finished, sender=GameJam)
        pre_save.connect(set_final_theme_when_jam_prepared, sender=GameJam)
        pre_save.connect(set_random_themes_for_jam_when_it_created, sender=GameJam)

    """ Функции тестирования """

    def test_game_list(self):
        """ Функция тестирования списка джемов """
        response = self.client.get(reverse('jams_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/jams_pages/jams.html')
        self.assertContains(response, self.jam_case_1.title)
        self.assertContains(response, self.jam_case_2.title)

    def test_jam_detail(self):
        """ Функция тестирования страницы джема """
        response = self.client.get(reverse('gamejam_detail', kwargs={'uuid':self.jam_case_1.uuid}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('pages/jams_pages/gamejam_detail.html')
        self.assertContains(response, self.jam_case_1.title)
        self.assertContains(response, self.jam_case_1.theme)
        self.assertContains(response, self.user.username)

    def test_jam_upload(self):
        """ Функция тестирования загрузки проекта """
        game_file = SimpleUploadedFile("test.zip", b"file_content", content_type="application/zip")
        response = self.client.post(reverse('upload-game', args=[self.jam_case_1.uuid]), {'game': game_file})
        self.assertRedirects(response, reverse("gamejam_detail", kwargs={'uuid': self.jam_case_1.uuid}))
        upload_file_exists = Game.objects.filter(user=self.user, jam_uuid=self.jam_case_1).exists()
        self.assertTrue(upload_file_exists)

    def test_upload_game_file_invalid_extension(self):
        """ Функция тестирования загрузки проекта с неправильными данными """
        game_file = SimpleUploadedFile("test_game.txt", b"file_content", content_type="text/plain")
        response = self.client.post(reverse('upload-game', args=[self.jam_case_1.uuid]),
                                    {'game': game_file})
        self.assertEqual(response.status_code, 404)

    def test_upload_game_file_no_file(self):
        """ Функция тестирования загрузки проекта с без данных """
        response = self.client.post(reverse('upload-game', args=[self.jam_case_1.uuid]), {})
        self.assertEqual(response.status_code, 404)

    def test_rate_jam_success(self):
        """ Функция тестирования выставления оценки на проект """
        response = self.client.post(reverse('count_stars', args=[self.jam_case_3.uuid, self.user2.id]),
                                    {'stars': 5})
        self.assertRedirects(response, reverse('gamejam_detail', args=[self.jam_case_3.uuid]))
        rating = RatingUserJam.objects.get(jam_uuid=self.jam_case_3, user=self.user2, user_who_rate=self.user)

        self.assertEqual(rating.stars, 5)

    def test_count_stars(self):
        """ Функция тестирования подсчёта средней оценки """
        expected_result = [
            {'user__username': 'testuser', 'user__id': 1, 'avg_rating': 4.0},
            {'user__username': 'user2', 'user__id': 2, 'avg_rating': 3.0}
        ]

        result = count_final_rating(self.jam_case_3.uuid)

        self.assertEqual(result[0], expected_result[0])
        self.assertEqual(result[1], expected_result[1])


class TestGameJamModels(TestCase):
    def setUp(self):
        post_init.disconnect(post_init_previous_jam_status_handler, sender=GameJam)
        pre_save.disconnect(calculate_winner_when_jam_finished, sender=GameJam)
        pre_save.disconnect(set_final_theme_when_jam_prepared, sender=GameJam)
        pre_save.disconnect(set_random_themes_for_jam_when_it_created, sender=GameJam)

        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def tearDown(self):
        post_init.connect(post_init_previous_jam_status_handler, sender=GameJam)
        pre_save.connect(calculate_winner_when_jam_finished, sender=GameJam)
        pre_save.connect(set_final_theme_when_jam_prepared, sender=GameJam)
        pre_save.connect(set_random_themes_for_jam_when_it_created, sender=GameJam)

    def test_model_gamejam_pr(self):
        jam_case_1 = GameJam.objects.create(
            uuid=uuid.uuid4(),
            title="Summer Game Jam 2023",
            date_start=datetime.now(),
            date_end=(datetime.now() + timedelta(days=3)),
            theme="Space Exploration",
            status='PR',
        )
        jam_case_1.users.set([self.user])
        self.assertEqual(str(jam_case_1), 'Summer Game Jam 2023' + ' - ' + "Space Exploration")
        self.assertTrue(isinstance(jam_case_1, GameJam))
