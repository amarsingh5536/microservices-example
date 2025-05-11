import json
import pika
import time
import os
import importlib
from events_app.utils import handle_pubsub_error

class RabbitMQBroker:
    def __init__(self):
        self.SUBSCRIBER_MAP = self.load_subscribers()
        self.rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
        self.rabbitmq_user = os.getenv("RABBITMQ_USER")
        self.rabbitmq_pwd = os.getenv("RABBITMQ_PWD")
        self.rabbitmq_port = int(os.getenv("RABBITMQ_PORT", 5674))

    @staticmethod
    def load_subscribers():
        """Load the subscriber function mappings from JSON file"""
        try:
            with open("pubsub/subscriber.json", "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Failed to load subscriber mappings: {e}")
            return {}

    
    def get_connection(self):
        credentials = pika.PlainCredentials(self.rabbitmq_user, self.rabbitmq_pwd)
        parameters = pika.ConnectionParameters(
            self.rabbitmq_host, self.rabbitmq_port, '/', credentials
        )

        def connect_with_retry():
            try:
                connection = pika.BlockingConnection(parameters)
                return connection
            except Exception:
                print("Connection to RabbitMQ failed. Retrying in 5 seconds...")
                time.sleep(5)
                return connect_with_retry()

        return connect_with_retry()

    def publish(self, routing_key, data,  exchange=''):
        connection = self.get_connection()
        channel = connection.channel()

        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=json.dumps(data))
        connection.close()

    def execute_callback(self, topic, data):
        """Dynamically import and execute callback function from subscriber.py"""
        callback_name = self.SUBSCRIBER_MAP.get(topic)

        if callback_name:
            module = importlib.import_module("pubsub.subscriber")
            callback_func = getattr(module, callback_name, None)

            if callable(callback_func):
                callback_func(data)
            else:
                print(f"Function '{callback_name}' not found in subscriber module.")
        else:
            print(f"No valid callback found for topic: {topic}")

    def message_handler(self, channel, method, properties, body):
        """Handler to consume messages from RabbitMQ and execute dynamic callbacks"""
        data = json.loads(body)
        topic = method.routing_key

        try:
            self.execute_callback(topic, data)
            # On success, delete any existing error log
            handle_pubsub_error(queue_name=topic, event=data, error=None, is_delete=True)
        except Exception as error:
            print(f"Error processing message from {topic}: {error}")
            # Save error log and publish updated event
            event = handle_pubsub_error(queue_name=topic, event=data, error=error)
            self.publish(topic, event)

        channel.basic_ack(delivery_tag=method.delivery_tag)

    def consume_messages(self):
        """Main method to subscribe to queues and consume messages"""
        connection = self.get_connection()
        channel = connection.channel()

        # Declare queues dynamically from the REGISTERED_TOPICS
        for topic in self.SUBSCRIBER_MAP.keys():
            channel.queue_declare(queue=topic, durable=True)

            channel.basic_consume(queue=topic, on_message_callback=self.message_handler)

        print("Waiting for messages...")
        channel.start_consuming()
