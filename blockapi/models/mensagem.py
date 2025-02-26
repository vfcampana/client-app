from sqlalchemy import Column, Integer, String, ForeignKey
from extensions import Base

class Mensagens(Base):
    __tablename__ = 'mensagens'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_chat = Column(Integer, ForeignKey('chat.id'))
    conteudo = Column(String, nullable=False)
    id_remetente = Column(Integer, ForeignKey('usuario.id'))