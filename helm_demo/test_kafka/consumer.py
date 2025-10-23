import os
import json
import logging
from kafka import KafkaConsumer
from kafka.errors import KafkaError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KafkaMessageConsumer:
    def __init__(self):
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.topic = os.getenv('KAFKA_TOPIC', 'test-topic')
        self.group_id = os.getenv('CONSUMER_GROUP_ID', 'test-consumer-group')
        
        # Initialize consumer with configuration
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset='earliest',  # Start from beginning if no offset
            enable_auto_commit=True,
            auto_commit_interval_ms=1000,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            # Consumer session timeout
            session_timeout_ms=30000,
            heartbeat_interval_ms=10000,
            # Max records to fetch per poll
            max_poll_records=100
        )
        logger.info(f"Connected to Kafka at {self.bootstrap_servers}")
        logger.info(f"Consuming from topic: {self.topic}")
        logger.info(f"Consumer group: {self.group_id}")
    
    def consume_messages(self):
        """Continuously consume messages"""
        try:
            logger.info("Starting to consume messages...")
            for message in self.consumer:
                self.process_message(message)
        except KafkaError as e:
            logger.error(f"Kafka error occurred: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            self.close()
    
    def process_message(self, message):
        """Process received message"""
        logger.info(
            f"Received message: "
            f"topic={message.topic} "
            f"partition={message.partition} "
            f"offset={message.offset} "
            f"key={message.key}"
        )
        logger.info(f"Message value: {message.value}")
        
        # Extract message data
        try:
            msg_id = message.value.get('id')
            timestamp = message.value.get('timestamp')
            data = message.value.get('data')
            
            logger.info(f"Processing: ID={msg_id}, Time={timestamp}, Data={data}")
            
            # Add your custom processing logic here
            # For example: save to database, trigger actions, etc.
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    def close(self):
        """Close consumer connection"""
        self.consumer.close()
        logger.info("Consumer closed")

if __name__ == "__main__":
    consumer = KafkaMessageConsumer()
    try:
        consumer.consume_messages()
    except KeyboardInterrupt:
        logger.info("Shutting down consumer...")
        consumer.close()
