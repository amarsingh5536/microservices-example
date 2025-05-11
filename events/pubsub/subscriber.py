from datetime import datetime
from events_app.utils import send_template_email, create_notification

def subscribe_send_template_email(data):
    send_template_email(data)

def subscribe_create_notification(data):
    create_notification(data)
