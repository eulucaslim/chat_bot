from app.lib.ChatBot import ChatBot
from app.models.Message import Message
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/send_message")
def send_message(msg: Message):
    try:
        chat = ChatBot()
        response = chat.send_message(msg.contents)
        return JSONResponse(content={"msg": str(response)}, status_code=200)
    except Exception as e:
        print(e)