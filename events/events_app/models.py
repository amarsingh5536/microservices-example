import enum
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON, TEXT
from sqlalchemy.orm import relationship
from . import db


class EventType(enum.Enum):
    webinar = "webinar"
    workshop = "workshop"
    conference = "conference"
    meetup = "meetup"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, comment="Event title")
    description = db.Column(db.Text, nullable=True, comment="Event description")
    event_type = db.Column(db.Enum(EventType), nullable=False, comment="Type of event (Enum)")
    start_time = db.Column(db.DateTime, nullable=False, comment="Event start time")
    end_time = db.Column(db.DateTime, nullable=True, comment="Event end time")
    location = db.Column(db.String(255), nullable=True, comment="Event location")
    created_by = db.Column(db.Integer, nullable=False, comment="User ID who created the event")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment="Event creation timestamp")
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow, comment="Event update timestamp")

    attendees = relationship("EventAttendee", backref="event")

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

class EventAttendee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id", ondelete="CASCADE"), nullable=False, comment="ForeignKey Event.id")
    user_id = db.Column(db.Integer, nullable=False, comment="User ID attending the event")
    registered_at = db.Column(db.DateTime, default=datetime.utcnow, comment="Timestamp when user registered")

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

class EmailTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    template_code = db.Column(db.String(50), nullable=True)
    html = db.Column(TEXT, nullable=True)
    subject = db.Column(db.String(250), nullable=True)
    cc_recipients = db.Column(db.Text, nullable=True, comment="Comma-separated CC emails")
    is_active = db.Column(db.Boolean(), default=True)

class NotificationTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    template_code = db.Column(db.String(50), nullable=True)
    html = db.Column(TEXT, nullable=True)
    is_active = db.Column(db.Boolean(), default=True)

class NotificationType(enum.Enum):
    """
    Notification types.
    """
    Info = 'Info'
    Warning = 'Warning'
    Success = 'Success'
    Error = 'Error'
    Other = 'Other'

class Services(enum.Enum):
    """
    All Services.
    """
    User = 1
    Event = 2

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, comment="User ID receiving the notification")
    actor_id = db.Column(db.Integer, nullable=True, comment="User who triggered the notification")
    actor_name = db.Column(db.String(250), nullable=True, comment="Actor's name")
    actor_image = db.Column(db.String(500), nullable=True, comment="URL of actor's picture")
    title = db.Column(db.String(250), nullable=True)
    message = db.Column(db.Text, nullable=False, comment="Notification message content")
    meta_data = db.Column(JSON, nullable=True, comment="Extra metadata for the notification")
    notification_type = db.Column(db.Enum(NotificationType), nullable=False, comment="Type of notification")
    redirect_url = db.Column(db.String(500), nullable=True, comment="URL to redirect on click")
    template_code = db.Column(db.String(50), nullable=True, comment="Unique code for message template")
    service = db.Column(db.Enum(Services), nullable=True)
    is_read = db.Column(db.Boolean, default=False, comment="Notification read status")
    is_send = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


class PubsubLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    queue_name = db.Column(db.String(100), nullable=True)
    event_name = db.Column(db.String(100), nullable=True)
    error_count = db.Column(db.Integer, nullable=True, default=0)
    statusCode = db.Column(db.String(100), nullable=True, default='500')
    queue_msg = db.Column(TEXT, nullable=True)
    error = db.Column(TEXT, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)