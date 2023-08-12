from django.test import TestCase

from apps.reports.serializer import ListReportSerializer


class ReportSerializerTestCase(TestCase):

    def test_serializer_with_valid_data(self):
        report_data = {
            'id': '1e382b20-226f-4b44-a0a9-6b67a89d389c',
            'average_image_processing_time': 12.0,
            'average_image_size': 12121,
            'average_image_labels_count': 4,
            'last_logged_users_count': 2,
            'last_joined_users_count': 23,
        }

        serializer = ListReportSerializer(data=report_data)

        self.assertTrue(serializer.is_valid())

    def test_serializer_with_no_valid_data(self):
        report_data = {
            'id': '1e382b20-226f-4b44-a0a9-6b67a89d389c',
            'average_image_processing_time': 12.0,
            'average_image_size': 12121,
            'last_logged_users_count': 2,
            'last_joined_users_count': 23,
        }

        serializer = ListReportSerializer(data=report_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('average_image_labels_count', serializer.errors)

    def test_create_report(self):
        report_data = {
            'id': '1e382b20-226f-4b44-a0a9-6b67a89d389c',
            'average_image_processing_time': 12.0,
            'average_image_size': 12121,
            'average_image_labels_count': 4,
            'last_logged_users_count': 2,
            'last_joined_users_count': 23,
        }

        serializer = ListReportSerializer(data=report_data)

        self.assertTrue(serializer.is_valid())
        created_report = serializer.save()

        self.assertEqual(created_report.average_image_processing_time, 12.0)
        self.assertEqual(created_report.average_image_size, 12121)
        self.assertEqual(created_report.average_image_labels_count, 4)
        self.assertEqual(created_report.last_logged_users_count, 2)
        self.assertEqual(created_report.last_joined_users_count, 23)
