import json
import threading
import os
import importlib
from confluent_kafka import Producer, Consumer, KafkaError
from confluent_kafka.admin import AdminClient, ConfigResource
from pubsub.topics import REGISTERED_TOPICS
import logging
logger = logging.getLogger(__name__)

class KafkaBroker:
    def __init__(self):
        self.kafka_broker = os.getenv("KAFKA_BROKER", "localhost:9092")
        self.CONSUMED_TOPICS=[]
        self.SUBSCRIBER_MAP={}
        
        # Kafka Producer Configuration
        self.producer_config = {
            'bootstrap.servers': self.kafka_broker,
            'linger.ms': 10,  # Wait up to 10ms to batch messages
            'batch.num.messages': 10000,  # Batch up to 10,000 messages
            'queue.buffering.max.messages': 100000,  # Increase buffer size
        }
        
        # Kafka Consumer Configuration
        self.consumer_config = {
            'bootstrap.servers': self.kafka_broker,
            'group.id': 'flask_group',
            'auto.offset.reset': 'latest',
            'enable.auto.commit': False,
            # 'auto.commit.interval.ms': 5000, # Auto commit interval 5s when 'enable.auto.commit' is True

            'session.timeout.ms': 45000,  # Increase timeout to prevent unnecessary rebalance
            'heartbeat.interval.ms': 10000,  # Ensures Kafka knows the consumer is alive send heartbeats every 10s.
            'max.poll.interval.ms': 600000,   # Prevents Consumers are removed due to slow processing 
        }

        self.load_subscriber_config("pubsub/subscriber.json")
        
        # Initialize Kafka Producer
        self.producer = Producer(**self.producer_config)
        self.consumer = Consumer(**self.consumer_config)
        self.consumer.subscribe(self.CONSUMED_TOPICS)

        # Kafka Admin Client (For Retention Updates)
        self.admin_client = AdminClient({'bootstrap.servers': self.kafka_broker})

    def load_subscriber_config(self, config_file):
        try:
            with open(config_file, 'r') as f:
                self.SUBSCRIBER_MAP = json.load(f)
                self.CONSUMED_TOPICS = list(self.SUBSCRIBER_MAP.keys())
        except Exception as e:
            logger.error(f"Error loading subscriber config: {e}")


    def on_delivery(self, err, msg):
        if err is not None:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def publish(self, topic, message):
        self.producer.produce(topic, 
                    key=str(message.get('user_id')), 
                    value=json.dumps(message), 
                    # callback=self.on_delivery
                )
        self.producer.flush()
    
    def execute_callback(self, topic, data):
        """Dynamically import and execute callback function from subscriber.py"""
        callback_name = self.SUBSCRIBER_MAP.get(topic)

        if callback_name:
            module = importlib.import_module("pubsub.subscriber")
            callback_func = getattr(module, callback_name, None)

            if callable(callback_func):
                callback_func(data)
            else:
                logger.warning(f"Function '{callback_name}' not found in subscriber module.")
        else:
            logger.warning(f"No valid callback found for topic: {topic}")

    def consume_messages(self):
        """Kafka consumer that listens for messages and processes them."""
        consumer = self.consumer

        while True:
            # Poll for messages with a timeout of 2 seconds
            msg = consumer.poll(2.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Consumer error: {msg.error()}")
                    continue
            try:
                data = json.loads(msg.value().decode('utf-8'))
                topic = msg.topic()
                self.execute_callback(topic, data)
                logger.info(f"Received message: {data} from topic: {topic}")
            except Exception as e:
                logger.error(f"Error processing message: {e}", msg.topic())

            consumer.commit(asynchronous=True) # To asynchronous false: commit(asynchronous=False) 
        