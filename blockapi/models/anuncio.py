from sqlalchemy import Column, Integer, Date, ForeignKey
from . import Base

class Anuncio(Base):
    __tablename__ = 'anuncio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_produto = Column(Integer, nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id'))
    data_criacao = Column(Date, nullable=False)
    data_alteracao = Column(Date, nullable=False)

