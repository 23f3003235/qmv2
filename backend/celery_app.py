from celery import Celery

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0'
)

celery.conf.update(
    timezone='Asia/Kolkata',
    enable_utc=False,
)

from app import app
from application.models import Users
from mail import send_mail
import csv

@celery.task()
def generate_csv(data, filename='report.csv'):
    import time
    time.sleep(5)
    with open(filename, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    send_mail('raj@gmail.com', 'Here\'s your csv export', 'Download your csv here http://127.0.0.1:5000/static/raj.csv')

@celery.task()
def daily_remainders():
    with app.app_context():
        users = Users.query.all()
        for user in users:
            send_mail(user.email, "visit","hi click")
    print('mails sent')

@celery.task()
def monthly_report():
    with app.app_context():
        users = Users.query.all()
        for user in users:
            data = [
                {'no': 1, 'name': 'rel'},
                {'no': 2, 'name': 'sel'},
                {'no': 3, 'name': 'tel'}
            ]
            template = """
here s the month act 
{% for activity in data %}
    {{ activity.no }} - {{ activity.name }}
{% endfor %}
"""
            from jinja2 import Template
            send_mail(user.email, "visit",Template(template).render(data=data))
    print('mails sent')

#scheduled tasks

from datetime import timedelta
from celery.schedules import crontab

celery.conf.beat_schedule = {
    'send_daily_reminders': {
        'task': 'celery_app.daily_remainders',
        # 'schedule': timedelta(seconds=3)
        'schedule': crontab(hour=17, minute=30)
    },
        'send_monthly_report': {
        'task': 'celery_app.monthly_report',
        'schedule': timedelta(seconds=60)
        # 'schedule': crontab(hour=15, minute=14, day_of_month=1)
    }
}


