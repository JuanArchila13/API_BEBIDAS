"""
    Definición del modelo Drink para la conexión con la base de datos.
    Este modelo representa la tabla de bebidas y sus atributos.
"""

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase
from db import engine

class Base(DeclarativeBase):
    pass

class Drink(Base): # pylint: disable=too-few-public-methods
    """
    Clase Drink que representa la tabla de bebidas en la base de datos.
    Esta clase hereda de declarative_base() de SQLAlchemy y define los atributos

    Args:
        Base (_type_): Clase base de SQLAlchemy para la declaración de modelos.
    """
    __tablename__ = "drinks"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, index=True)
    size = Column(String(50))
    price = Column(Float)

Base.metadata.create_all(engine)
