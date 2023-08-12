from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.reports.models import AnalyticReport
from apps.reports.serializer import ListReportSerializer


class ReportViewSet(viewsets.ViewSet):
    queryset = AnalyticReport.objects.all()

    def list(self, request):
        serializer = ListReportSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
