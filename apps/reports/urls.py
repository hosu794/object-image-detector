from django.urls import path

from apps.reports.views import ReportViewSet

urlpatterns = [
    path('', ReportViewSet.as_view({'get': 'list'}), name='report-list'),
]
