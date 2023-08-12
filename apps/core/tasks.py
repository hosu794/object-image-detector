from celery import shared_task


@shared_task
def my_celery_task(amount_of_tasks):
    return f"Task completed successfully! {amount_of_tasks}"
