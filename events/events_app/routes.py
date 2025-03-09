from . import app
from .api import (EventView, EventDetailView)

# Register the API routes
app.add_url_rule("/api/events/", view_func=EventView.as_view("event_view"))
app.add_url_rule("/api/events/<int:event_id>/", view_func=EventDetailView.as_view("event_detail_view"))
