from rest_framework import status

from apps.core.tests.base import BaseApiTestCase
from apps.reports.models import AnalyticReport
from apps.reports.serializer import ListReportSerializer
from rest_framework.reverse import reverse


class ReportListViewTest(BaseApiTestCase):

    def setUp(self):
        super().setUp()

    def test_get_reports_list(self):
        AnalyticReport.objects.create(average_image_processing_time=10.2, average_image_size=2323,
                                      average_image_labels_count=12,
                                      last_logged_users_count=234,
                                      last_joined_users_count=33)

        AnalyticReport.objects.create(average_image_processing_time=232.2, average_image_size=233232,
                                      average_image_labels_count=22,
                                      last_logged_users_count=222,
                                      last_joined_users_count=111)

        reports = AnalyticReport.objects.all()

        serializer = ListReportSerializer(reports, many=True)

        response = self.authorized_client.get(reverse('report-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
