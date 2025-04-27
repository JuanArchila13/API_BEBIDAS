"""
Representación de un DTO (Data Transfer Object) para una bebida.
Este DTO se emplea para transferir datos con otras aplicaciones o con una interfaz de usuario (UI).
"""
from pydantic import BaseModel

class DrinkDTO(BaseModel):
    """
    Clase que representa un DTO (Data Transfer Object) para una bebida.
    Args:
        BaseModel (_type_): Clase base de Pydantic para la validación de datos.
    """
    name: str
    size: str
    price: float
