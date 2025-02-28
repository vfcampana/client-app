from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from models.usuario import Usuario

# Carregar variáveis de ambiente
load_dotenv()

# Obter URL do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")

# Criar o engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Criar uma factory para sessões do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return SessionLocal().query(Usuario).get(user_id)
