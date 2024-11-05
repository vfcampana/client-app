from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from datetime import datetime

from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

url = URL.create(
    drivername="",
    username="",
    host="",
    database="",
    password="",
    port=23939
)

engine = create_engine(url)
conection = engine.connect()