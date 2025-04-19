from fastapi import FastAPI, HTTPException
from models.drink import Drink

from db import session

app = FastAPI()

@app.post("/menu")
async def create_drink(name: str, size: str, price: float):
    if name == "":
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if price < 0:
        raise HTTPException(status_code=400, detail="Price must be greater than 0")
    
    drink = Drink(name=name, size=size, price=price)
    session.add(drink)
    session.commit()
    return {"message": "Drink created successfully", "drink": drink}

@app.get("/menu")
async def obtain_menu():
    drinks = session.query(Drink).all()
    return drinks

@app.get("/menu/{name}")
async def obtain_drink(name: str):
    drink = session.query(Drink).filter(Drink.name == name).first()
    if not drink:
        raise HTTPException(status_code=404, detail="Drink not found")
    return drink