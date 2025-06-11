from app.config.settings import KAFKA_BROKER
from app.models.producer import ProduceMessage
from kafka import KafkaProducer
from fastapi import HTTPException
import json

# Constant Values Section
KAFKA_TOPIC = 'fastapi-topic'
PRODUCER_CLIENT_ID = 'fastapi_producer'

def serializer(message: json) -> str:
    return json.dumps(message).encode()

producer = KafkaProducer(
    api_version=(0, 8, 0),
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=serializer,
    client_id=PRODUCER_CLIENT_ID
)

def produce_kafka_message(messageRequest: ProduceMessage):
    try:
        producer.send(KAFKA_TOPIC, json.dumps({'message': messageRequest.message}))
        producer.flush() # Ensures all messages are sent
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Failed to send message")