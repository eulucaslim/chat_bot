from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from app.services.message_service import MessageService

app = FastAPI(
    title="ChatBot in Python!",
    version="1.0.0"
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