import uuid
from datetime import datetime, timedelta
from unittest import skip

from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import redirect
from django.test import TestCase
from django.urls import reverse
from jams.models import GameJam, Game, RatingUserJam
from jams.views import count_final_rating
from users.models import User


class JamsViewTest(TestCase):
    def setUp(self):
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

    def test_game_list(self):
        response = self.client.get(reverse('jams_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/jams_pages/jams.html')
        self.assertContains(response, self.jam_case_1.title)
        self.assertContains(response, self.jam_case_2.title)

    def test_jam_detail(self):
        response = self.client.get(reverse('gamejam_detail', kwargs={'uuid':self.jam_case_1.uuid}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('pages/jams_pages/gamejam_detail.html')
        self.assertContains(response, self.jam_case_1.title)
        self.assertContains(response, self.jam_case_1.theme)
        self.assertContains(response, self.user.username)

    def test_jam_upload(self):
        game_file = SimpleUploadedFile("test.zip", b"file_content", content_type="application/zip")
        response = self.client.post(reverse('upload-game', args=[self.jam_case_1.uuid]), {'game': game_file})
        self.assertRedirects(response, reverse('jams_list'))
        upload_file_exists = Game.objects.filter(user=self.user, jam_uuid=self.jam_case_1).exists()
        self.assertTrue(upload_file_exists)

    def test_upload_game_file_invalid_extension(self):
        game_file = SimpleUploadedFile("test_game.txt", b"file_content", content_type="text/plain")
        response = self.client.post(reverse('upload-game', args=[self.jam_case_1.uuid]),
                                    {'game': game_file})
        self.assertEqual(response.status_code, 404)

    def test_upload_game_file_no_file(self):
        response = self.client.post(reverse('upload-game', args=[self.jam_case_1.uuid]), {})
        self.assertEqual(response.status_code, 404)

    def test_rate_jam_success(self):
        response = self.client.post(reverse('count_stars', args=[self.jam_case_3.uuid, self.user2.id]),
                                    {'stars': 5})
        self.assertRedirects(response, reverse('gamejam_detail', args=[self.jam_case_3.uuid]))
        rating = RatingUserJam.objects.get(jam_uuid=self.jam_case_3, user=self.user2, user_who_rate=self.user)

        self.assertEqual(rating.stars, 5)

    def test_final_rating(self):
        expected_result = [
            {'username': 'testuser', 'avg_rating': 4},
            {'username': 'user2', 'avg_rating': 3}
        ]

        result = count_final_rating(self.jam_case_3.uuid)

        self.assertEqual(result, expected_result)
