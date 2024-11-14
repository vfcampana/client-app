from datetime import datetime
from sqlalchemy.orm import declarative_base
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from database import engine


Base = declarative_base()


class CompanyUser(Base, UserMixin):
    __tablename__ = 'company_users'

    id = Column(Integer, primary_key=True, unique=True)
    razao_social = Column(String(80), nullable=True)
    cnpj = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    senha = Column(String(80), nullable=False)
    telefones = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    registrado = Column(DateTime, default=datetime.now)
    atualizado = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    qtd_blocos = Column(Integer, default=0)
    role = Column(String(80), nullable=False, default='user')

    def to_dict(self):
        return {
            "id": self.id,
            "razao_social": self.razao_social,
            "cnpj": self.cnpj,
            "email": self.email,
            "senha": self.senha,
            "telefones": self.telefones,
            "is_active": self.is_active,
            "registrado": self.registrado,
            "atualizado": self.atualizado,
            "qtd_blocos": self.qtd_blocos,
            "role": self.role
        }

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Example query to get all active company users
active_company = session.query(CompanyUser).filter_by(is_active=True).all()

for company in active_company:
    print(company.to_dict())

session.close()