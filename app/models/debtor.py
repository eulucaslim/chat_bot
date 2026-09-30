from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class Debtor(BaseModel):
    name: str
    value: Decimal
    date: datetime

