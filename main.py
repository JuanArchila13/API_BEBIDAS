""" 
Modulo principal de la API de bebidas.
Este modulo contiene la configuracion de la API, las rutas y los controladores para manejar las solicitudes HTTP.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.drink import Drink
from dto.drink_dto import DrinkDTO
from db import session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/menu")
async def obtain_menu():
    """
    Obtiene la lista de todas las bebidas en el menú.

    Returns:
        list: Lista de objetos Drink que representan las bebidas en el menú.
    """
    drinks = session.query(Drink).all()
    return drinks

@app.get("/menu/{name}")
async def obtain_drink(name: str):
    """
    Obtiene una bebida específica del menú a partir de un nombre.

    Args:
        name (str): Nombre de la bebida a buscar.

    Raises:
        HTTPException: Si la bebida no se encuentra en el menú.

    Returns:
        dict: Objeto Drink con los datos de la bebida solicitada.
    """
    drink = session.query(Drink).filter(Drink.name == name).first()
    if not drink:
        raise HTTPException(status_code=404, detail="Drink not found")
    return drink

@app.post("/menu")
async def create_drink(drink: DrinkDTO):
    """
    Crea una nueva bebida en el menú.

    Args:
        drink (DrinkDTO): Objeto que contiene los datos de la bebida, 
                          incluyendo nombre, tamaño y precio.

    Raises:
        HTTPException: Si el nombre está vacío o el precio es menor a 0.

    Returns:
        dict: Mensaje de éxito y los datos de la bebida creada.
    """
    if drink.name == "":
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if drink.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than 0")

    drink_to_create = Drink(name=drink.name, size=drink.size, price=drink.price)
    session.add(drink_to_create)
    session.commit()
    return {"message": "Drink created successfully", "drink": drink_to_create}