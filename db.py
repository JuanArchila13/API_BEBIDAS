"""
    Conexión con la base de datos MySQL 
    utilizando SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="123456789",
    host="localhost",
    database="drinks_db",
    port=3306,
)

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()
