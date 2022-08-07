import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TorLinkRotator.settings')


app = Celery('TorLinkRotator')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'cleanup_expired_links': {
        'task': 'TorLinkRotator.apps.rotator.tasks.cleanup_expired_links.cleanup_expired_links',
        'schedule': crontab(minute="*/1"),
        'args': ()
    },
}
