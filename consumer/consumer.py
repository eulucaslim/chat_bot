from app.config.settings import KAFKA_BROKER
from app.services.message_service import MessageService
from kafka import KafkaConsumer
import json


# Constant Values Section
KAFKA_TOPIC = 'message-chatbot'
KAFKA_GROUP_ID = 'group_chatbot'

class ConsumerKafka:
    
    def __init__(self):
        self.service = MessageService()
        self.consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest',
            group_id=KAFKA_GROUP_ID
        )

    def process_messages(self):
        if self.consumer:
            for msg in self.consumer:
                data = json.loads(msg.value.decode('utf-8'))
                self.service.process_message(data)
                print("Mensagem Processada!")
