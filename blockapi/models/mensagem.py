from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, JSON
from datetime import datetime
from models.base import Base

class Mensagem(Base):
    __tablename__ = 'mensagens'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversa_id = Column(Integer, ForeignKey('conversas.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=True)  # Nullable para mensagens do sistema
    conteudo = Column(Text, nullable=False)  # Renomeado de 'texto' para 'conteudo'
    tipo = Column(String(50), default='texto')
    enviada_em = Column(DateTime, default=datetime.utcnow, nullable=False)  # Renomeado de 'data_envio'
    lida = Column(Boolean, default=False)
    proposta_valor = Column(String(20), nullable=True)
    proposta_status = Column(String(20), default='pendente')
    metadata_json = Column(JSON, nullable=True)  # Para dados adicionais (blockchain, etc.)
    
    # Manter compatibilidade com campos antigos
    @property
    def texto(self):
        return self.conteudo
    
    @texto.setter
    def texto(self, value):
        self.conteudo = value
    
    @property
    def data_envio(self):
        return self.enviada_em
    
    @data_envio.setter
    def data_envio(self, value):
        self.enviada_em = value
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversa_id': self.conversa_id,
            'usuario_id': self.usuario_id,
            'conteudo': self.conteudo,
            'texto': self.conteudo,  # Compatibilidade
            'tipo': self.tipo,
            'enviada_em': self.enviada_em.isoformat() if self.enviada_em else None,
            'data_envio': self.enviada_em.isoformat() if self.enviada_em else None,  # Compatibilidade
            'lida': self.lida,
            'proposta_valor': self.proposta_valor,
            'proposta_status': self.proposta_status,
            'metadata': self.metadata_json
        }