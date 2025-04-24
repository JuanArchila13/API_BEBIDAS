import requests
from behave import given, when, then

DRINKS_API = "http://localhost:8000/menu"
ORDERS_API = "http://localhost:8080/orders"


@given('que la bebida "{drink}" está registrada en el menú')
def step_register_drink(context, drink):
    response = requests.post(DRINKS_API, json={
        "name": drink,
        "size": "250 ml",
        "price": 3000
    })
    assert response.status_code in [200, 201]

@given('que la bebida "{drink}" no está registrada en el menú')
def step_no_register_drink(context, drink):
    try:
        response = requests.get(f"{DRINKS_API}/{drink}", timeout=5)
        if response.status_code == 200:
            raise AssertionError(f"La bebida '{drink}' ya está registrada. No cumple el escenario negativo.")
        elif response.status_code == 404:
            context.drink_not_available = drink 
        else:
            raise Exception(f"Error inesperado al consultar la bebida: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        raise AssertionError(f"Error de red al consultar la bebida: {e}")

@when('realizo un pedido de "{drink}" desde la API de pedidos')
def step_make_order(context, drink):
    context.order_response = requests.post(ORDERS_API, json={
        "name": drink,
        "size": 1
    })

@then('el sistema debe aceptar el pedido con un código 200 o 201')
def step_verify_success(context):
    assert context.order_response.status_code in [200, 201]

@then('el sistema debe rechazar el pedido con un código 404 o mensaje de error')
def step_verify_failure(context):
    assert context.order_response.status_code in [404, 400, 422]
