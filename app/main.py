from threading import Thread
from app.config.settings import KAFKA_BROKER
from consumer.consumer import KAFKA_TOPIC
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from kafka import KafkaProducer
from confluent_kafka import Consumer
import json


app = FastAPI(
    title="ChatBot in Python!",
    version="1.0.0"
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

messages = []

def kafka_consumer():
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'mygroup',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe(['test-topic'])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        # Armazena a mensagem em memória
        messages.append(msg.value().decode('utf-8'))

# Inicia o consumer em background
Thread(target=kafka_consumer, daemon=True).start()

@app.post("/receive_message", tags=['Webhook'])
async def receive_message(
    request: Request
):
    try:
        payload = await request.json()
        producer.send(KAFKA_TOPIC, payload)
        producer.flush()
        return JSONResponse(content={"message": "The message send to broker!"}, status_code=200)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

@app.get("/results")
async def results():
    return {"messages": messages}