from rest_framework import status
from rest_framework.reverse import reverse

from apps.core.tests.base import BaseApiTestCase


class AuthCoreTest(BaseApiTestCase):

    def test_protected_url(self):
        response = self.authorized_client.get(reverse('protected'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_access(self):
        response = self.unauthorized_client.get(reverse('protected'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
