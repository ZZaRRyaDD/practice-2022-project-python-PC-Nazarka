from config.celery import app, schedules


app.conf.beat_schedule = {
   'interest_append': {
        'task': 'apps.targets.tasks.interest_append',
        'schedule': schedules.crontab(minute=0, hour=0),
   },
}
