"""
Test para la aplicación FastAPI que maneja un menú de bebidas.
Este módulo contiene pruebas unitarias para verificar el correcto funcionamiento de las rutas 
y la lógica de negocio de la API.
"""

from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from main import app
from models.drink import Drink
from db import session

# Crear un cliente de pruebas para la aplicación FastAPI
client = TestClient(app)

# Se le indica a la session que use un mock para evitar la conexión a la base de datos real
session.query = MagicMock() # type: ignore[method-assign]

def test_obtain_drinks_success():
    """
    Test para verificar que la ruta /menu devuelve correctamente la lista de bebidas 
    registradas en la base de datos.
    """
    # Lista de bebidas a simular
    mock_drinks = [
        Drink(name="Sprite", size="12 Oz", price=13000),
        Drink(name="Coca-Cola", size="8 Oz", price=8000),
        Drink(name="Pepsi", size="14 Oz", price=15000),
        Drink(name="Manzana Postobon", size="6 Oz", price=5000),
    ]
    # Configurar el mock para devolver la lista de bebidas simuladas
    session.query().all.return_value = mock_drinks
    # Hacer una petición GET a la ruta /menu para obtener la lista de bebidas registradas en
    # la base de datos
    response = client.get("/menu")
    # Verificar que el status de la respuesta es 200 (OK)
    assert response.status_code == 200
    # Verificar que el tamaño de la respuesta en formato JSON es 4 (es decir, hay 4 bebidas)
    assert len(response.json()) == 4
    # Verificar que las bebidas traidas en la respuesta son las mismas que las bebidas simuladas
    assert response.json() == [
        {"name": "Sprite", "size": "12 Oz", "price": 13000},
        {"name": "Coca-Cola", "size": "8 Oz", "price": 8000},
        {"name": "Pepsi", "size": "14 Oz", "price": 15000},
        {"name": "Manzana Postobon", "size": "6 Oz", "price": 5000},
    ]

def test_obtain_drink_success():
    """
    Test para verificar que la ruta /menu/{name} devuelve correctamente una bebida específica 
    registrada en la base de datos.
    """
    # Mock de la bebida simulada
    mock_drink = Drink(name="Coca-Cola", size="10 Oz", price=12000)
    # Configurar el mock para devolver la bebida simulada
    session.query().filter().first.return_value = mock_drink
    # Hacer una petición GET a la ruta /menu/{name} para obtener la bebida específica
    response = client.get("/menu/Coca-Cola")
    # Verificar que el status de la respuesta es 200 (OK)
    assert response.status_code == 200
    # Verificar que la bebida traida en la respuesta es la misma que la bebida simulada
    assert response.json() == {
        "name": "Coca-Cola",
        "size": "10 Oz",
        "price": 12000
    }

def test_obtain_drink_not_found():
    """
    Test para verificar que la ruta /menu/{name} devuelve un error 404 si la bebida no se 
    encuentra en la base de datos.
    """
    # Configurar el mock para devolver None
    session.query().filter().first.return_value = None
    #  Hacer una petición GET a la ruta /menu/{name} con una bebida que no existe
    response = client.get("/menu/nonexistent_drink")
    # Verificar que el status de la respuesta es 404 (No encontrado)
    assert response.status_code == 404
    # Verificar que el mensaje de error es "Drink not found"
    assert response.json() == {"detail": "Drink not found"}

def test_create_drink_success():
    """
    Test para verificar que la ruta /menu crea correctamente una bebida en la 
    base de datos.
    """
    # Configurar el mock para simular la creación de una bebida
    session.add = MagicMock()
    # Configurar el mock para simular la confirmación de la sesión
    session.commit = MagicMock()
    # Hacer una petición POST a la ruta /menu para crear una nueva bebida
    response = client.post("/menu", json={"name": "Pepsi", "size": "12 Oz", "price": 6000})
    # Verificar que el status de la respuesta es 200 (OK)
    assert response.status_code == 200
    # Verificar que la bebida creada es la misma que la bebida enviada en la petición,
    # además de obtener el mensaje de éxito
    assert response.json() == {
        "message": "Drink created successfully",
        "drink": {
            "name": "Pepsi",
            "size": "12 Oz",
            "price": 6000
        }
    }

def test_create_drink_empty_name():
    """
    Test para verificar que la ruta /menu devuelve un error 400 si el nombre de la 
    bebida está vacío.
    """
    # Configurar el mock para simular la creación de una bebida
    session.add = MagicMock()
    # Configurar el mock para simular la confirmación de la sesión
    session.commit = MagicMock()
    # Hacer una petición POST a la ruta /menu con un nombre vacío
    response = client.post("/menu", json={"name": "", "size": "12 Oz", "price": 6000})
    # Verificar que el status de la respuesta es 400 (Bad Request)
    assert response.status_code == 400
    # Verificar que el mensaje de error es "Name cannot be empty"
    assert response.json() == {"detail": "Name cannot be empty"}

def test_create_drink_negative_price():
    """
    Test para verificar que la ruta /menu devuelve un error 400 si el precio de la bebida 
    es negativo.
    """
    # Hacer una petición POST a la ruta /menu con un precio negativo
    response = client.post("/menu", json={"name": "Pepsi", "size": "12 Oz", "price": -1.0})
    # Verificar que el status de la respuesta es 400 (Bad Request)
    assert response.status_code == 400
    # Verificar que el mensaje de error es "Price must be greater than 0"
    assert response.json() == {"detail": "Price must be greater than 0"}
