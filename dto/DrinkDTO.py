from pydantic import BaseModel

class DrinkDTO(BaseModel):
    name: str
    size: str
    price: float