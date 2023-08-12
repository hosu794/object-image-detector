from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken

from apps.users.models import User


class BaseApiTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="test123",
            email="test123@email.com",
            password="password"
        )

        self.token = AccessToken.for_user(self.user)

        self.authorized_client = APIClient()

        self.authorized_client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.token)}')

        self.unauthorized_client = APIClient()

