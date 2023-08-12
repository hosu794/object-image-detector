import datetime

from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.reverse import reverse
from freezegun import freeze_time

from apps.core.tests.base import BaseApiTestCase


class AuthTestCase(BaseApiTestCase):
    REGISTER_URL_NAME = 'REGISTER_URL_NAME'
    TOKEN_URL_NAME = "TOKEN_URL_NAME"
    REFRESH_URL_NAME = 'REFRESH_URL_NAME'

    def setUp(self):
        super().setUp()

        self.url_names = {
            self.REGISTER_URL_NAME: reverse('register'),
            self.TOKEN_URL_NAME: reverse('token_obtain_pair'),
            self.REFRESH_URL_NAME: reverse('token_refresh')
        }

    def test_register(self):
        data = {
            'email': 'register_test@email.com',
            'username': 'register_test',
            'password': 'password123',
            'confirm_password': 'password123'
        }

        response = self.unauthorized_client.post(self.url_names[self.REGISTER_URL_NAME], data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_confirm_password_register(self):
        data = {
            'email': 'register_test@email.com',
            'username': 'register_test',
            'password': 'password123',
            'confirm_password': 'not_same_password'
        }

        response = self.unauthorized_client.post(self.url_names[self.REGISTER_URL_NAME], data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        data = {
            'email': 'test123@email.com',
            'password': 'password'
        }
        response = self.unauthorized_client.post(self.url_names[self.TOKEN_URL_NAME], data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_login(self):
        data = {
            'email': 'test123@email.com',
            'password': 'wrongpassword'
        }
        response = self.unauthorized_client.post(self.url_names[self.TOKEN_URL_NAME], data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        refresh_data = {
            'refresh': str(TokenObtainPairSerializer().get_token(self.user))
        }

        refresh_response = self.unauthorized_client.post(self.url_names[self.REFRESH_URL_NAME], refresh_data)

        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

    def test_expired_refresh_token(self):
        refresh_data = {
            'refresh': str(RefreshToken().for_user(self.user))
        }

        with freeze_time(datetime.datetime.now() + datetime.timedelta(days=1)):
            refresh_response = self.unauthorized_client.post(self.url_names[self.REFRESH_URL_NAME], refresh_data)

        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
