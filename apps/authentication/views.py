from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from apps.authentication.serializer import RegisterSerializer, UserSerializer
from django.contrib.auth.models import update_last_login


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh_token = RefreshToken().for_user(user)
        token_access = AccessToken().for_user(user)

        update_last_login(None, user)

        return Response({
            "user": UserSerializer(user).data,
            'refresh': str(refresh_token),
            'access': str(token_access),
        })
