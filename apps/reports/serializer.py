from rest_framework import serializers

from apps.reports.models import AnalyticReport


class ListReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticReport
        fields = ['id', 'average_image_processing_time', 'average_image_size', 'average_image_labels_count',
                  'last_logged_users_count', 'last_joined_users_count']
