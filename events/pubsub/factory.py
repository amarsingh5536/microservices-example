import os
import threading
from .brokers.kafka import KafkaBroker
from .brokers.rabbitmq import RabbitMQBroker
from .topics import REGISTERED_TOPICS 
import logging

# Set up logger
logger = logging.getLogger(__name__)


MESSAGING_SYSTEM = os.getenv("MESSAGING_SYSTEM", "rabbitmq").lower()  # Default to rabbitmq

class PubsubFactory:
    def __init__(self):
        self.broker = self._get_broker()

    def _get_broker(self):
        """Factory method to get the appropriate broker based on the environment."""
        if MESSAGING_SYSTEM == "kafka":
            return KafkaBroker()
        elif MESSAGING_SYSTEM == "rabbitmq":
            return RabbitMQBroker()
        else:
            raise ValueError(f"Unsupported messaging system: {MESSAGING_SYSTEM}")

    def publish(self, topic, message):
        """Publish a message to a topic."""
        if topic not in REGISTERED_TOPICS:
            logger.error(f"Topic '{topic}' is not registered.")
            return
        try:
            self.broker.publish(topic, message)
            logger.info(f"Published message to topic '{topic}': {message}")
        except Exception as e:
            logger.error(f"Failed to publish message to topic '{topic}': {e}")

    def start_subscriber(self):
        """Start the subscriber to listen for messages and execute callbacks."""
        self.broker.consume_messages()