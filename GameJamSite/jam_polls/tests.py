import uuid
from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from jam_polls.models import Question
from jams.models import GameJam
from users.models import User


class PollViewTest(TestCase):
    def setUp(self):
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
        self.question1 = Question.objects.create(question_text='Question 1', jam_uuid=self.jam_case_1)
        self.question2 = Question.objects.create(question_text='Question 2', jam_uuid=self.jam_case_1)
        self.url = reverse('poll', kwargs={'uuid': self.jam_case_1.uuid})

    def test_poll_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/jam_polls_pages/poll.html')
        self.assertContains(response, Question.objects.get(id=1).question_text)

    def test_submit_poll(self):
        response = self.client.post(reverse('submit', kwargs={'uuid':self.jam_case_1.uuid}), {'question_id':
                                                                                              self.question1.id,
                                                                                              'answer': '1'})
        self.assertEqual(response.status_code, 200)
        self.question1.refresh_from_db()
        self.assertEqual(self.question1.count, 1)
        self.assertEqual(response.json()['question_id'], self.question2.id)

        response = self.client.post(reverse('submit', kwargs={'uuid': self.jam_case_1.uuid}), {'question_id':
                                                                                                   self.question2.id,
                                                                                               'answer': '-1'})
        self.assertEqual(response.status_code, 200)
        self.question1.refresh_from_db()
        self.assertEqual(self.question2.count, 0)

    def test_submit_poll_all_questions_completed(self):
        response = self.client.post(reverse('submit', kwargs={'uuid': self.jam_case_1.uuid}),
                                    {'question_id': self.question2.id, 'answer': '1'})
        self.assertEqual(response.status_code, 200)
        self.jam_case_1.refresh_from_db()
        self.assertIn(self.user, self.jam_case_1.users.all())

        self.assertEqual(response.json()['message'], 'Все вопросы пройдены')
        self.assertTrue(response.json()['redirect'])
