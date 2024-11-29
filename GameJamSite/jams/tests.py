import uuid
from datetime import datetime, timedelta
from unittest import skip

from django.test import TestCase
from django.urls import reverse
from jams.models import GameJams
from users.models import User


class JamsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.jam_case_1 = GameJams.objects.create(
            uuid=uuid.uuid4(),
            title="Summer Game Jam 2023",
            date_start=datetime.now(),
            date_end=(datetime.now() + timedelta(days=3)),
            theme="Space Exploration",
            status='OG'
        )
        self.jam_case_2 = GameJams.objects.create(
            uuid=uuid.uuid4(),
            title="Summer Game Jam 2024",
            date_start=datetime.now(),
            date_end=(datetime.now() + timedelta(days=3)),
            theme="Exploration",
            status='PR'
        )
        self.jam_case_1.users.set([self.user])
        #для пользователей нужно его авторизовать самому

    def test_game_list(self):
        response = self.client.get(reverse('jams_list'))
        self.assertEqual(response.status_code, int(200))
        self.assertTemplateUsed(response, 'pages/jams_pages/jams.html')
        self.assertContains(response.content.decode(), self.jam_case_1.title)
        self.assertContains(response.content.decode(), self.jam_case_2.title)

    def test_jam_detail(self):
        response = self.client.get(reverse('gamejam_detail',
                                           kwargs={'uuid':self.jam_case_1.uuid}))
        self.assertEqual(response.status_code, int(200))
        self.assertTemplateUsed('pages/jams_pages/gamejam_detail.html')
