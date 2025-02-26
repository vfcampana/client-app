from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Criar instância do SQLAlchemy
Base = declarative_base()

# Obter URL do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")

# Criar o engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Criar uma factory para sessões do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
