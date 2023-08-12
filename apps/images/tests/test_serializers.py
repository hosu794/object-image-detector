from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.images.models import Image
from apps.images.serializer import ImageCreateUpdateSerializer, ImageLabelSerializer
from apps.users.models import User


class ImageSerializerTestCase(TestCase):

    def test_serializer_with_valid_data(self):
        user = User.objects.create_user(username='testuser3', email='testuser@example.com', password='testpass')
        image_data = {
            'id': '1e382b20-226f-4b44-a0a9-6b67a89d389c',
            'image': SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
            'creator': user,
        }

        serializer = ImageCreateUpdateSerializer(data=image_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_without_image(self):
        user = User.objects.create_user(username='testuser2', email='testuser@example.com', password='testpass')
        image_data = {
            'id': '1e382b20-226f-4b44-a0a9-6b67a89d389c',
            'creator': user,
        }

        serializer = ImageCreateUpdateSerializer(data=image_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('image', serializer.errors)

    def test_create_image(self):
        user = User.objects.create_user(username='testuser1', email='testuser@example.com', password='testpass')
        image_data = {
            'id': '1e382b20-226f-4b44-a0a9-6b67a89d389c',
            'image': SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
        }

        serializer = ImageCreateUpdateSerializer(data=image_data)

        self.assertTrue(serializer.is_valid())
        created_image = serializer.save(creator=user)
        self.assertIsNotNone(created_image.id)
        self.assertIsNotNone(created_image.image)
        self.assertEqual(created_image.creator.username, "testuser1")
        self.assertEqual(created_image.creator.email, "testuser@example.com")
        self.assertEqual(created_image.status, Image.Status.PLANNED)


class ImageSerializersTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.image = Image.objects.create(image="path/to/image.jpg", creator=self.user)

    def test_serializer_with_valid_data(self):
        label = {
            'name': 'label_name',
            'confidence': 0.99,
            'x_cord': 120,
            'y_cord': 133,
        }

        serializer = ImageLabelSerializer(data=label)
        self.assertTrue(serializer.is_valid())

    def test_not_valid_label_serializer(self):
        label_data = {
            'name': 'label_name',
            'confidence': 0.87,
            'x_cord': 120
        }

        serializer = ImageLabelSerializer(data=label_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('y_cord', serializer.errors)
