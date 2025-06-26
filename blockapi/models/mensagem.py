from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from datetime import datetime
from models.base import Base

class Mensagem(Base):
    __tablename__ = 'mensagens'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversa_id = Column(Integer, ForeignKey('conversas.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    texto = Column(Text, nullable=False)
    tipo = Column(String(50), default='texto')
    data_envio = Column(DateTime, default=datetime.utcnow, nullable=False)
    lida = Column(Boolean, default=False)
    proposta_valor = Column(String(20), nullable=True)
    proposta_status = Column(String(20), default='pendente')
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversa_id': self.conversa_id,
            'usuario_id': self.usuario_id,
            'texto': self.texto,
            'tipo': self.tipo,
            'data_envio': self.data_envio.isoformat() if self.data_envio else None,
            'lida': self.lida,
            'proposta_valor': self.proposta_valor,
            'proposta_status': self.proposta_status
        }