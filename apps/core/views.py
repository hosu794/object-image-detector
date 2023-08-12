from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.core.tasks import my_celery_task


class ProtectedView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'protected'}
        return Response(content)


class CeleryTest(APIView):

    def get(self, request):
        my_celery_task.delay(10)

        content = {'message': 'protected'}
        return Response(content)
