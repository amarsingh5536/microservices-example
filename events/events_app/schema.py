from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from . import models, db

class EventSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.Event
        include_fk = True
        load_instance = True
        sqla_session = db.session

    start_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    end_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    created_by = fields.Integer(dump_only=True)  # Exclude from input validation
    event_type = fields.Method("get_event_type", deserialize="load_event_type")

    def get_event_type(self, obj):
        return obj.event_type.value if obj.event_type else None 

    def load_event_type(self, value):
        return models.EventType(value) 

class EventAttendeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.EventAttendee
        include_fk = True
        load_instance = True
        sqla_session = db.session

class EmailTemplateSchema(SQLAlchemyAutoSchema):
    """
    EmailTemplate schema.
    """

    class Meta:
        model = models.EmailTemplate
        sqla_session = db.Session
        include_fk = True
        load_instance = True

event_schema = EventSchema()
events_schema = EventSchema(many=True)
email_template_schema = EmailTemplateSchema()