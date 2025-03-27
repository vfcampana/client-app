from sqlalchemy import Column, Integer, Date, ForeignKey
from extensions import Base

class Anuncio(Base):
    __tablename__ = 'anuncio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_bloco = Column(Integer, nullable=True)
    id_lote = Column(Integer, nullable=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id'))
    data_criacao = Column(Date, nullable=False)
    data_alteracao = Column(Date, nullable=False)
    status = Column(Integer, nullable=False)

