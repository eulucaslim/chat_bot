from app.services.message_service import MessageService
from app.config.settings import KAFKA_ADMIN_CLIENT, KAFKA_BROKER
from app.models.producer import ProduceMessage
from app.utils.producer import produce_kafka_message, KAFKA_TOPIC
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from kafka.admin import KafkaAdminClient, NewTopic

@asynccontextmanager
async def lifespan(app: FastAPI):

    admin_client = KafkaAdminClient(
        bootstrap_servers=KAFKA_BROKER,
        client_id=KAFKA_ADMIN_CLIENT
    )
    if not KAFKA_TOPIC in admin_client.list_topics():
        admin_client.create_topics(
            new_topics=[
                NewTopic(
                    name=KAFKA_TOPIC,
                    num_partitions=1,
                    replication_factor=1
                )
            ],
            validate_only=False
        )
        # admin_client.delete_topics(topics=[KAFKA_TOPIC])
    yield # separation point

app = FastAPI(
    title="ChatBot in Python!",
    version="1.0.0",
    lifespan=lifespan
)


@app.post("/receive_message", tags=['Webhook'])
async def receive_message(
    request: Request, 
    message_service: MessageService = Depends()
):
    try:
        response = await request.json()
        await message_service.process_message(response)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

@app.post('/produce/message/', tags=["Produce Message"])
async def produce_message(messageRequest : ProduceMessage, background_tasks : BackgroundTasks):
    background_tasks.add_task(produce_kafka_message, messageRequest)
    return {"message": "Message Received, tahnk you for sending a message!"}