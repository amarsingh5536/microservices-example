from flask import request, jsonify, views
from flask_babel import lazy_gettext as _
from sqlalchemy import desc, or_, func, text, and_
from . import models, db, app
from .filters import *
from .schema import *


class EventView(views.MethodView):

    def get(self):
        """Fetch all events"""
        events = models.Event.query.order_by(desc(models.Event.start_time)).all()
        return jsonify({"message": "Events fetched successfully", "data": events_schema.dump(events)}), 200

    def post(self):
        """Create a new event"""
        data = request.json
        errors = event_schema.validate(data)
        if errors:
            return jsonify(errors), 400

        new_event = event_schema.load(data)
        new_event.created_by = request.user.id  

        db.session.add(new_event)
        db.session.commit()
        return jsonify({"message": "Event created successfully", "data": event_schema.dump(new_event)}), 201

class EventDetailView(views.MethodView):

    def get(self, event_id):
        """Fetch event details"""
        event = models.Event.query.get(event_id)
        if not event:
            return jsonify({"message": "Event not found"}), 404
        return jsonify({"message": "Event fetched successfully", "data": event_schema.dump(event)}), 200

    def put(self, event_id):
        """Update event details"""
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"message": "Event not found"}), 404

        data = request.json
        for key, value in data.items():
            setattr(event, key, value)

        db.session.commit()
        return jsonify({"message": "Event updated successfully", "data": event_schema.dump(event)}), 200

    def delete(self, event_id):
        """Delete an event"""
        event = models.Event.query.get(event_id)
        if not event:
            return jsonify({"message": "Event not found"}), 404

        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Event deleted successfully"}), 200

