import enum
from datetime import datetime
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

class NotificationType(enum.Enum):
    welcome = "welcome"
    event_update = "event_update"
    event_cancellation = "event_cancellation"
    reminder = "reminder"

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, comment="User ID receiving the notification")
    event_id = db.Column(db.Integer, db.ForeignKey("event.id", ondelete="CASCADE"), nullable=True, comment="Related Event ID")
    notification_type = db.Column(db.Enum(NotificationType), nullable=False, comment="Type of notification")
    message = db.Column(db.Text, nullable=False, comment="Notification message content")
    sent_at = db.Column(db.DateTime, default=datetime.utcnow, comment="Notification sent timestamp")
    is_read = db.Column(db.Boolean, default=False, comment="Notification read status")
    event = relationship("Event", backref="notifications")

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
