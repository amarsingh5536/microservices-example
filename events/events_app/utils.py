import io
import json
import base64
from io import BytesIO
from datetime import datetime, timedelta
from flask import render_template_string
from flask_mail import Message, Attachment
from .schema import email_template_schema
from . import models, db, app, mail


def send_template_email(data):
    """
    Accept email events from different services and send respective email notifications.
    """
    template_code = data.get('template_code')
    recipients = data.get('recipients', [])
    cc = data.get('cc', [])
    bcc = data.get('bcc', [])
    context = data.get('context', {})
    subject = data.get('subject')
    attachments = context.get('attachments', [])

    # Validate required fields
    if not template_code or not recipients:
        raise ValueError("Template code and recipients are required.")

    # Fetch and render the email template
    template_obj = models.EmailTemplate.query.filter_by(template_code=template_code).first()
    if not template_obj:
        raise ValueError(f"Email template with code '{template_code}' not found.")

    template_data = email_template_schema.dump(template_obj)
    body = render_template_string(template_data.get('html', ''), data=context)
    
    # Use template subject if not provided
    subject = subject or template_obj.subject

    # Construct email message
    msg = Message(
        subject=subject,
        sender=app.config.get('MAIL_SENDER_ID'),
        recipients=recipients,
        cc=cc,
        bcc=bcc
    )
    msg.html = body

    # Process and attach files
    for attachment in attachments:
        file = attachment.get("file")
        if file:
            header, encoded_data = file.split(';base64,')
            content_type = attachment.get('content_type', header.split(':')[1])
            file_name = attachment.get('file_name') or attachment.get("name", "attachment")

            decoded_file = base64.b64decode(encoded_data)
            msg.attach(filename=file_name, content_type=content_type, data=decoded_file)

    mail.send(msg)
    return {"success": True, "message": "Email sent successfully."}


def create_notification(data):
    """
    Creates a notification and saves it to the database.
    """
    notification_type = data.get('notification_type', 'Other').title()
    service_module = data.get('service', None)

    # Convert level to enum
    notification_type = (
        models.NotificationType[notification_type] 
        if notification_type in models.NotificationType.__members__ 
        else models.NotificationType.Other
    )

    # Convert service to enum
    service = (
        models.Services[service_module] 
        if service_module in models.Services.__members__ 
        else None
    )

    metadata = dict(data.get('metadata', {}))
    notification_json = {
        "user_id": data.get('user_id') or data.get('by_id'),
        "actor_id": data.get('by_id'),
        "actor_name": data.get('by_name'),
        "title": data.get('title'),
        "message": data.get('message'),
        "meta_data": metadata,
        "notification_type": notification_type,
        "redirect_url": data.get('redirect_url'),
        "template_code": data.get('template_code'),
        "service": service,
    }

    notification_instance = models.Notification(**notification_json)
    notification_instance.save()

    return {"success": True, "message": "Notification created successfully."}


def handle_pubsub_error(queue_name, event, error, is_delete=False):
    """
    Handle PubsubLogs errors.
        :param queue_name: PubsubLogs Queue Name.
        :param event: RabbitMQ Event/Queue message.
        :param error: Error.
        :param is_delete: Flag to delete the existing log.
        :return: Updated event with log_id and error_counts.
    """
    logs_obj = models.PubsubLogs.query.filter_by(id=event.get('error_log_id')).first()
    if is_delete:
        if logs_obj:
            db.session.delete(logs_obj)
            db.session.commit()
        return event

    if not logs_obj:
        logs_obj = models.PubsubLogs()

    logs_obj.queue_name = queue_name
    logs_obj.event_name = event.get('event') or 'send_email'
    logs_obj.error_count = logs_obj.error_count + 1 if logs_obj.error_count else 1
    logs_obj.queue_msg = str(event)
    logs_obj.error = str(error)

    db.session.add(logs_obj)
    db.session.commit()

    event['error_log_id'] = logs_obj.id  # Adding log id in event data for error record.
    event['error_counts'] = logs_obj.error_count  # Adding error count in event data for error record.
    return event