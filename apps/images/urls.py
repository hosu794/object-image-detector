from django.urls import path

from apps.images.views import ImageViewSet

urlpatterns = [
    path('', ImageViewSet.as_view({'get': 'list'}), name='image-list'),
    path('create', ImageViewSet.as_view({'post': 'create'}), name='image-create'),
    path('<uuid:pk>', ImageViewSet.as_view({'get': 'retrieve'}), name='image-detail'),
    path('update/<uuid:pk>', ImageViewSet.as_view({'put': 'update'}), name='image-update'),
    path('delete/<uuid:pk>', ImageViewSet.as_view({'delete': 'destroy'}), name='image-delete'),
]
