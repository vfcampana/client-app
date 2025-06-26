from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from models.base import Base

class Conversa(Base):
    __tablename__ = 'conversas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario1_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    usuario2_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    bloco_id = Column(Integer, ForeignKey('bloco.id'), nullable=True)
    criada_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    ultima_atividade = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'usuario1_id': self.usuario1_id,
            'usuario2_id': self.usuario2_id,
            'bloco_id': self.bloco_id,
            'criada_em': self.criada_em.isoformat() if self.criada_em else None,
            'ultima_atividade': self.ultima_atividade.isoformat() if self.ultima_atividade else None
        }