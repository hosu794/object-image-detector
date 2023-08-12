from django.urls import path

from apps.core import views

urlpatterns = [
    path('protected', views.ProtectedView.as_view(), name='protected'),
    path('celery', views.CeleryTest.as_view(), name='celery'),
]
