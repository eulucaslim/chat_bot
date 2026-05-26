from app.core.settings import CHATBOT_PORT
from app.routers import messages
from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="ChatBot in Python!",
    version="0.0.1"
)

app.include_router(messages.router, prefix="/api/v1")

if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=CHATBOT_PORT)