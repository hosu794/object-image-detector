
from django.db.models import Avg
from django.utils import timezone

from apps.images.models import ImageAnalytics
from apps.reports.models import AnalyticReport
from apps.users.models import User


class ReportService:

    @staticmethod
    def create_analytic_report():

        timedelta = ReportService._get_timedelta(minutes=2)

        image_analytics = ReportService._get_image_analytics_greater_then_timestamp(timedelta)

        last_joined_users_count, last_logged_users_count = ReportService._get_users_count_stats(timedelta)

        avg_labels_count, avg_processing_time, avg_size = ReportService._get_average_analytics_fields(analytics)

        return AnalyticReport.objects.create(average_image_processing_time=avg_processing_time, average_image_size=avg_size,
                                             average_image_labels_count=avg_labels_count,
                                             last_logged_users_count=last_logged_users_count,
                                             last_joined_users_count=last_joined_users_count)

    @staticmethod
    def _get_image_analytics_greater_then_timestamp(timedelta):
        return ImageAnalytics.objects.filter(created_at__gte=timedelta)

    @staticmethod
    def _get_timedelta(days=0, hours=0, minutes=0, seconds=0):
        current_time = timezone.now()
        timedelta = current_time - timezone.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        return timedelta

    @staticmethod
    def _get_users_count_stats(timedelta):
        last_logged_users_count = User.objects.filter(last_login__gte=timedelta).count()
        last_joined_users_count = User.objects.filter(date_joined__gte=timedelta).count()
        return last_joined_users_count, last_logged_users_count

    @staticmethod
    def _get_average_analytics_fields(analytics):
        avg_size = analytics.aggregate(Avg('size'))['size__avg'] or 0
        avg_processing_time = analytics.aggregate(Avg('processing_time'))['processing_time__avg'] or 0
        avg_labels_count = analytics.aggregate(Avg('labels_count'))['labels_count__avg'] or 0

        return avg_labels_count, avg_processing_time, avg_size

