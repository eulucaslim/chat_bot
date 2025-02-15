from pydantic import BaseModel

class Message(BaseModel):
    user: str
    contents: str