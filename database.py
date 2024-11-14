from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("DATABASE_URL")

engine = create_engine(url)

conection = engine.connect()