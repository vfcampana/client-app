from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import Base

class Favorito(Base):
    __tablename__ = 'favorito'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    id_bloco = Column(Integer, ForeignKey('bloco.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'id_usuario': self.id_usuario,
            'id_bloco': self.id_bloco
        }