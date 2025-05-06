from django.test import TestCase
from django.urls import reverse
from users.forms import RegisterUserForm, LoginUserForm
from users.models import User


class UserViewTest(TestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.username = 'user'
        self.password = 'password123'
        self.user = User.objects.create_user(
            email='test@example.com',
            username=self.username,
            password=self.password)

    def test_register_form(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        form = RegisterUserForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_register_form(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'differentpassword'
        }
        form = RegisterUserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_login_valid_user(self):
        login_data = {
            'email': 'test@example.com',
            'password': self.password
        }
        response = self.client.post(self.login_url, login_data)
        print('response', response)
        self.assertRedirects(response, reverse('profile_detail', kwargs={'username': self.user.username}))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_user_detail(self):
        self.client.login(username='user', password='password123')
        response = self.client.get(reverse('profile_detail', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('pages/jams_pages/user_detail.html')
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.email)

    def test_logout(self):
        self.client.logout()
        response = self.client.get(reverse('jams_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('pages/jam_pages/jams.html')
