from pydantic import BaseModel

class Message(BaseModel):
    user_number: str
    content: str

class Answer(BaseModel):
    user_id: str
    ai_response: str
