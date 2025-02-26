from sqlalchemy import Column, Integer, String, Float
from . import Base

class Lote(Base):
    __tablename__ = 'lote'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    observacoes = Column(String)
