import os
import json
from kafka import KafkaProducer
import httpx
import time

KAFKA_BROKER = os.environ['KAFKA_BROKER']
API_MAIN_URL = os.environ['API_MAIN_URL']
API_BRANCH_URL = os.environ['API_BRANCH_URL']
TOPIC = 'test-topic'

producer = KafkaProducer({'bootstrap.servers': KAFKA_BROKER})

def send_test_message(payload):
    producer.send(TOPIC, value=json.dumps(payload).encode('utf-8'))
    producer.flush()

test_payloads = [
    {"input": "teste1"},
    {"input": "teste2"},
    {"input": "teste3"},
]

for payload in test_payloads:
    send_test_message(payload)

print("Esperando 5 segundos para ler as mensagens ")
time.sleep(5)

with httpx.Client() as client:
    main_resp = client.get(f"{API_MAIN_URL}/results").json()
    branch_resp = client.get(f"{API_BRANCH_URL}/results").json()

if main_resp != branch_resp:
    print("Diferença encontrada!")
    print("Main:", main_resp)
    print("Branch:", branch_resp)
    exit(1)
else:
    print("Respostas iguais.")