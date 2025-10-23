import os
import json
import time
import logging
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KafkaMessageProducer:
    def __init__(self):
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.topic = os.getenv('KAFKA_TOPIC', 'test-topic')
        # Initialize producer with configuration
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            acks='all',  # Wait for all replicas to acknowledge
            retries=3,
            max_in_flight_requests_per_connection=1
        )
        logger.info(f"Connected to Kafka at {self.bootstrap_servers}")
    
    def send_message(self, key, value):
        """Send message to Kafka topic"""
        try:
            future = self.producer.send(
                self.topic,
                key=key,
                value=value
            )
            
            # Block for 'synchronous' sends
            record_metadata = future.get(timeout=10)
            logger.info(
                f"Message sent to topic={record_metadata.topic} "
                f"partition={record_metadata.partition} "
                f"offset={record_metadata.offset}"
            )
            return True
        except KafkaError as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    def produce_messages(self):
        """Continuously produce messages"""
        counter = 0
        while True:
            message = {
                'id': counter,
                'timestamp': datetime.now().isoformat(),
                'data': f'Message {counter}'
            }
            
            key = f"key-{counter}"
            self.send_message(key, message)
            
            counter += 1
            time.sleep(5)  # Send message every 5 seconds
    
    def close(self):
        """Close producer connection"""
        self.producer.flush()
        self.producer.close()
        logger.info("Producer closed")

if __name__ == "__main__":
    producer = KafkaMessageProducer()
    try:
        producer.produce_messages()
    except KeyboardInterrupt:
        logger.info("Shutting down producer...")
        producer.close()