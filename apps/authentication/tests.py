from datetime import timedelta

from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from apps.authentication.models import User, UserToken


class PasswordResetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.request_url = reverse('authentication:password-reset')
        self.confirm_url = reverse('authentication:password-reset-confirm')
        self.user = User.objects.create_user(email='reset@example.com', password='oldpass1')

    def confirm(self, token, password='newpass1', password2=None):
        return self.client.post(self.confirm_url, {
            'token': token,
            'password': password,
            'password2': password2 or password,
        }, format='json')

    def test_request_sends_email_with_link(self):
        response = self.client.post(self.request_url, {'email': 'RESET@example.com'}, format='json')

        self.assertEqual(response.status_code, 200)
        token = UserToken.objects.get(user=self.user).token
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['reset@example.com'])
        self.assertIn(f'/password-reset/{token}/', mail.outbox[0].body)

    def test_request_for_unknown_email_looks_the_same(self):
        known = self.client.post(self.request_url, {'email': 'reset@example.com'}, format='json')
        unknown = self.client.post(self.request_url, {'email': 'nobody@example.com'}, format='json')

        self.assertEqual(unknown.status_code, 200)
        self.assertEqual(unknown.data, known.data)
        self.assertEqual(len(mail.outbox), 1)

    def test_request_needs_valid_email(self):
        response = self.client.post(self.request_url, {'email': 'not-an-email'}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_confirm_changes_password_once(self):
        token = UserToken.objects.create(user=self.user).token

        response = self.confirm(token)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass1'))

        again = self.confirm(token, 'otherpass1')
        self.assertEqual(again.status_code, 400)

    def test_confirm_cancels_older_links(self):
        old_token = UserToken.objects.create(user=self.user).token
        new_token = UserToken.objects.create(user=self.user).token

        self.assertEqual(self.confirm(new_token).status_code, 200)
        self.assertEqual(self.confirm(old_token, 'otherpass1').status_code, 400)

    def test_confirm_rejects_expired_link(self):
        user_token = UserToken.objects.create(user=self.user)
        UserToken.objects.filter(pk=user_token.pk).update(created_at=timezone.now() - timedelta(hours=2))

        response = self.confirm(user_token.token)

        self.assertEqual(response.status_code, 400)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('oldpass1'))

    def test_confirm_rejects_unknown_token(self):
        self.assertEqual(self.confirm('nope').status_code, 400)

    def test_confirm_checks_passwords(self):
        token = UserToken.objects.create(user=self.user).token

        self.assertEqual(self.confirm(token, 'newpass1', 'newpass2').status_code, 400)
        self.assertEqual(self.confirm(token, '123').status_code, 400)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('oldpass1'))
