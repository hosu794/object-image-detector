from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.images.models import Image
from apps.images.serializer import ImageCreateUpdateSerializer, ImageSerializerWithLabels
from rest_framework import viewsets

from apps.images.tasks import process_image


class ImageViewSet(viewsets.ViewSet):
    queryset = Image.objects.prefetch_related('imagelabel_set').all()

    @method_decorator(cache_page(60 * 2))
    def list(self, request):
        serializer = ImageSerializerWithLabels(self.queryset, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 2))
    def retrieve(self, request, pk=None):
        image = get_object_or_404(self.queryset, pk=pk)
        serializer = ImageSerializerWithLabels(image)
        return Response(serializer.data)

    def create(self, request):
        serializer = ImageCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.save(creator=request.user)

        process_image.delay(image.id)

        return Response(serializer.data, status=201)

    def destroy(self, request, pk=None):
        image = get_object_or_404(self.queryset, pk=pk)
        image.delete()
        return Response(status=204)

    def update(self, request, pk=None):
        image = get_object_or_404(self.queryset, pk=pk)
        serializer = ImageCreateUpdateSerializer(image, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
