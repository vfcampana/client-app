from sqlalchemy import Column, Integer, ForeignKey
from extensions import Base

class Chat(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_anuncio = Column(Integer, ForeignKey('anuncio.id'))
    id_cliente = Column(Integer, ForeignKey('usuario.id'))
