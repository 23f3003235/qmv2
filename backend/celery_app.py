from celery import Celery

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0'
)
from app import app
from application.models import Users
from mail import send_mail



def daily_remainders():
    with app.app_context():
        users = Users.query.all()
        for user in users:
            send_mail(user.email, "visit","hi click")
    print('mails sent')

def monthly_report():
    with app.app_context():
        users = Users.query.all()
        for user in users:
            data = [
                {'no': 1, 'name': 'rel'},
                {'no': 2, 'name': 'sel'},
                {'no': 3, 'name': 'tel'}
            ]
            template = """here s the act 
            {% for activity in data %}
                {{ activity no }} - {{ activity.name }}
            {% endfor %}
            """
            from jinja2 import Template
            send_mail(user.email, "visit","monthly report")
    print('mails sent')

daily_remainders()
monthly_report()