import json
from pubsub.factory import PubsubFactory

def publish_event(event_key, data):
    """Generic pubsub producer function."""
    producer = PubsubFactory()
    producer.publish(event_key, data)