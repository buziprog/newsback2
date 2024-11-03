from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Replace 'core' if your project name is different
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')  # Again replace 'core' if your project name is different

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Add periodic task scheduling
app.conf.beat_schedule = {
    'fetch_and_store_articles_every_5_minutes': {
        # Replace with your actual task name
        'task': 'Articles.tasks.fetch_and_store_articles',
        'schedule': crontab(minute='*/5'),
    },
}
