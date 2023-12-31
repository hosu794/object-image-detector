from django.urls import path

from apps.authentication.views import RegisterApi
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
      path('register', RegisterApi.as_view(), name='register'),
      path('token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
      path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
