from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app
from models.drink import Drink
from db import session

# Crear un cliente de pruebas para la aplicación FastAPI
client = TestClient(app)

# Mock de la sesión de base de datos
session.query = MagicMock()

def test_obtain_drink_not_found():
    # Configurar el mock para devolver None
    session.query().filter().first.return_value = None

    # Realizar la solicitud GET
    response = client.get("/menu/nonexistent_drink")

    # Verificar que devuelve un error 404
    assert response.status_code == 404
    assert response.json() == {"detail": "Drink not found"}

def test_obtain_drink_success():
    # Configurar el mock para devolver una bebida simulada
    mock_drink = Drink(name="Coca-Cola", size="10 Oz", price=12000)
    session.query().filter().first.return_value = mock_drink

    # Realizar la solicitud GET
    response = client.get("/menu/Coca-Cola")

    # Verificar que devuelve la bebida correcta
    assert response.status_code == 200
    assert response.json() == {
        "name": "Coca-Cola",
        "size": "10 Oz",
        "price": 12000
    }

def test_create_drink_success():
    # Configurar el mock para simular la creación de una bebida
    session.add = MagicMock()
    session.commit = MagicMock()

    # Realizar la solicitud POST
    response = client.post("/menu", json={"name": "Pepsi", "size": "12 Oz", "price": 6000})

    # Verificar que la bebida se creó correctamente
    assert response.status_code == 200
    assert response.json() == {
        "message": "Drink created successfully",
        "drink": {
            "name": "Pepsi",
            "size": "12 Oz",
            "price": 6000
        }
    }

def test_create_drink_empty_name():
    # Realizar la solicitud POST con un nombre vacío
    response = client.post("/menu", json={"name": "", "size": "12 Oz", "price": 6000})

    # Verificar que devuelve un error 400
    assert response.status_code == 400
    assert response.json() == {"detail": "Name cannot be empty"}

def test_create_drink_negative_price():
    # Realizar la solicitud POST con un precio negativo
    response = client.post("/menu", json={"name": "Pepsi", "size": "12 Oz", "price": -1.0})

    # Verificar que devuelve un error 400
    assert response.status_code == 400
    assert response.json() == {"detail": "Price must be greater than 0"}