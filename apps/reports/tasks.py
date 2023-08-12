from celery import shared_task
from apps.reports.report_service import ReportService


@shared_task(name='create_report')
def create_timestamp_report():
    return ReportService.create_analytic_report()
