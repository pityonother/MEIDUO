import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","meiduo_mail.settings")

from celery import Celery
app=Celery('celery_tasks')
app.config_from_object('celery_tasks.config')

app.autodiscover_tasks(['celery_tasks.sms'])

