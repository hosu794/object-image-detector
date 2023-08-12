from django.contrib import admin

from apps.reports.models import AnalyticReport


class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'average_image_processing_time', 'average_image_size', 'average_image_labels_count',
                    'last_logged_users_count', 'last_joined_users_count']


admin.site.register(AnalyticReport, ReportAdmin)