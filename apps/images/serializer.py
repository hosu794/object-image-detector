from rest_framework import serializers

from apps.images.models import Image, ImageLabel


class ImageCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']


class ImageLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageLabel
        fields = ('id', 'name', 'confidence', 'x_cord', 'y_cord')


class ImageSerializerWithLabels(serializers.ModelSerializer):
    labels = ImageLabelSerializer(many=True, read_only=True, source='imagelabel_set')

    class Meta:
        model = Image
        fields = ('id', 'image', 'creator', 'created_at', 'updated_at', 'status', 'labels')
