from django.contrib import admin

from apps.images.models import Image, ImageLabel, ImageAnalytics


class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'created_at', 'updated_at', 'creator']


admin.site.register(Image, ImageAdmin)


class ImageLabelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'confidence', 'x_cord', 'y_cord', 'image']


admin.site.register(ImageLabel, ImageLabelAdmin)


class ImageAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['id', 'processing_time', 'size', 'image', 'labels_count']


admin.site.register(ImageAnalytics, ImageAnalyticsAdmin)
