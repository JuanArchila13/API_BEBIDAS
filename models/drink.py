from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from db import engine

Base = declarative_base()

class Drink(Base):
    __tablename__ = "drinks"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, index=True)
    size = Column(String(50))
    price = Column(Float)

Base.metadata.create_all(engine)