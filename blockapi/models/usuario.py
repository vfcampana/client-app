import datetime
from sqlalchemy import Column, Integer, String, Date
from models.base import Base
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    documento = Column(String, nullable=False, unique=True)
    email = Column(String, unique=True)
    telefone = Column(String, nullable=False, unique=True)
    cep = Column(String, nullable=False)
    logradouro = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    pais = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    data_registro = Column(Date, nullable=False, default=datetime.datetime.now())
    estado = Column(String, nullable=False)

    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)