from sqlalchemy import Column, Integer, String, Float, ForeignKey
from models.base import Base

class Lote(Base):
    __tablename__ = 'lote'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    observacoes = Column(String)
    id_usuario = Column(Integer, ForeignKey('usuario.id'))
    status = Column(String, nullable=False)


    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'preco': self.preco,
            'observacoes': self.observacoes,
            'id_usuario': self.id_usuario,
            'status': self.status
        }