from pydantic import BaseModel

class User(BaseModel):
    phone_number: int
    text: str