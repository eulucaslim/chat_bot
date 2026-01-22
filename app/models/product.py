from pydantic import BaseModel, field_validator

class Product(BaseModel):
    name: str
    quantity: int
    price: float
    MIN_VALUE: int = 0

    field_validator("quantity")
    @classmethod    
    def validate_quantity(cls, quantity: str):
        if not quantity.isdigit():
            raise ValueError("The quantity is not valid, please enter the integer number")
        if int(quantity) <= cls.MIN_VALUE:
            raise ValueError("The input value cannot be less than or equal to 0.")
        return int(quantity)
    
    field_validator("pricce")
    @classmethod    
    def validate_quantity(cls, price: str):
        if not price.isdigit():
            raise ValueError("The price is not valid, please enter the decimal number")
        if float(price) <= cls.MIN_VALUE:
            raise ValueError("The input value cannot be less than or equal to 0.")
        return float(price)