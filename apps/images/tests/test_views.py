from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.reverse import reverse
from apps.core.tests.base import BaseApiTestCase
from apps.images.models import Image, ImageLabel
from apps.images.serializer import ImageSerializerWithLabels
from apps.celery import app as celery_app


class ImageCreateViewTest(BaseApiTestCase):

    def setUp(self):
        super().setUp()
        self.image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        celery_app.conf.update(CELERY_ALWAYS_EAGER=True)

    def test_create_image(self):
        response = self.authorized_client.post(reverse('image-create'), {'image': self.image_file}, format='multipart')
        self.assertIn('id', response.data)
        self.assertIn('image', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(Image.objects.first().creator, self.user)

    def test_create_image_unauthenticated(self):
        response = self.unauthorized_client.post(reverse('image-create'), {'image': self.image_file},
                                                 format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Image.objects.count(), 0)


class ImageListViewTest(BaseApiTestCase):

    def test_get_image_list(self):
        image1 = Image.objects.create(image='path/to/image1.png', creator=self.user)
        image2 = Image.objects.create(image='path/to/image2.png', creator=self.user)

        ImageLabel.objects.create(
            name="label_name",
            confidence=0.95,
            x_cord=100,
            y_cord=150,
            image=image1
        )

        ImageLabel.objects.create(
            name="label_name2",
            confidence=0.95,
            x_cord=100,
            y_cord=150,
            image=image2
        )

        images = Image.objects.prefetch_related('imagelabel_set').all()
        serializer = ImageSerializerWithLabels(images, many=True)

        response = self.authorized_client.get(reverse('image-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class ImageDetailViewDetail(BaseApiTestCase):

    def test_get_image_detail(self):
        image = Image.objects.create(image='path/to/your/image.png', creator=self.user)

        ImageLabel.objects.create(
            name="label_name2",
            confidence=0.95,
            x_cord=100,
            y_cord=150,
            image=image
        )

        response = self.authorized_client.get(reverse('image-detail', kwargs={'pk': image.pk}))
        serializer = ImageSerializerWithLabels(image)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class ImageUpdateViewTest(BaseApiTestCase):

    def test_update_image(self):
        created_image = Image.objects.create(image='path/to/your/image.png', creator=self.user)

        update_file = SimpleUploadedFile("update_file.jpg", b"file_content", content_type="image/jpeg")

        response = self.authorized_client.put(reverse('image-update', kwargs={'pk': created_image.pk}),
                                              {'image': update_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        created_image.refresh_from_db()

        self.assertIn('image', response.data)
        self.assertIn('id', response.data)

        self.assertEqual(response.data['id'], str(created_image.id))


class ImageDestroyViewTest(BaseApiTestCase):

    def test_delete_image(self):
        image = Image.objects.create(image='path/to/your/image.png', creator=self.user)

        response = self.authorized_client.delete(reverse('image-delete', kwargs={'pk': image.pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Image.objects.count(), 0)

    def test_not_authorized_delete_image(self):
        image = Image.objects.create(image='path/to/your/delete.png', creator=self.user)

        response = self.unauthorized_client.delete(reverse('image-delete', kwargs={'pk': image.pk}))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
