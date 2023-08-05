from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class CloudinaryTestCase(TestCase):
    ENDPOINT = '/auth/login'

    def setUp(self) -> None:
        super().setUp()

        self.user = User.objects.create_user('test', password='test123')
        self.admin_user = User.objects.create_superuser('testadmin', password='test123',
                                                        is_active=True)
        Token(user=self.admin_user).save()
        Token(user=self.user).save()

    def get_client(self, user, http_authorization_prefix='Token'):
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION='%s %s' % (http_authorization_prefix, user.auth_token.key))
        return c

    def test_token(self):
        data = {'username': 'test', 'password': 'test123'}

        resp = self.client.post(self.ENDPOINT, data=data)
        self.assertIn('token', resp.data, resp.content)

    def test_masquerade(self):
        data = {'user_id': self.user.id}
        client = self.get_client(self.admin_user)

        resp = client.post('/auth/masquerade', data=data)

        self.assertIn('token', resp.data, resp.content)

    def test_masquerade_when_non_superuser_tries(self):
        data = {'user_id': self.admin_user.id}
        client = self.get_client(self.user)

        resp = client.post('/auth/masquerade', data=data)

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN, resp.content)
