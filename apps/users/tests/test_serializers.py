from unittest import TestCase

from apps.users.models import User
from apps.authentication.serializer import UserSerializer


class UserSerializerTestCase(TestCase):

    def test_serialization(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        serializer = UserSerializer(instance=user)
        expected_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
        }
        self.assertEqual(serializer.data, expected_data)
