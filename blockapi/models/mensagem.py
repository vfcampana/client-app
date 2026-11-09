from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, JSON
from datetime import datetime
from models.base import Base

class Mensagem(Base):
    __tablename__ = 'mensagens'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversa_id = Column(Integer, ForeignKey('conversas.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=True)
    texto = Column(Text, nullable=False)
    tipo = Column(String(50), default='texto')
    data_envio = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Compatibilidade com campos novos (para futuras migrações)
    @property
    def conteudo(self):
        return self.texto
    
    @conteudo.setter
    def conteudo(self, value):
        self.texto = value
    
    @property
    def enviada_em(self):
        return self.data_envio
    
    @enviada_em.setter
    def enviada_em(self, value):
        self.data_envio = value
    
    # Campos virtuais para funcionalidades extras (não na BD)
    @property
    def lida(self):
        return False  # Sempre False por enquanto
    
    @property
    def proposta_valor(self):
        return None  # Não implementado na BD atual
    
    @property
    def proposta_status(self):
        return 'pendente'  # Valor padrão
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversa_id': self.conversa_id,
            'usuario_id': self.usuario_id,
            'texto': self.texto,
            'conteudo': self.texto,  # Compatibilidade
            'tipo': self.tipo,
            'data_envio': self.data_envio.isoformat() if self.data_envio else None,
            'enviada_em': self.data_envio.isoformat() if self.data_envio else None,  # Compatibilidade
            'lida': self.lida,
            'proposta_valor': self.proposta_valor,
            'proposta_status': self.proposta_status
        }