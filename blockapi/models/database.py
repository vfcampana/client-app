from sqlalchemy.orm import relationship
from models.extensions import engine, SessionLocal
from models.base import Base
from models.bloco import Bloco
from models.usuario import Usuario
from models.imagem import Imagens
from models.anuncio import Anuncio
from models.lote_bloco import LoteBlocos
from models.lote import Lote
from models.mensagem import Mensagem
from models.conversa import Conversa

# Exportar Session para compatibilidade
Session = SessionLocal

# Definição dos relacionamentos dentro de uma função
def define_relationships():
    # Relacionamentos existentes
    Usuario.blocos = relationship("Bloco", back_populates="usuario")
    Bloco.usuario = relationship("Usuario", back_populates="blocos")
    Bloco.imagens = relationship("Imagens", back_populates="bloco")
    Imagens.bloco = relationship("Bloco", back_populates="imagens")
    Usuario.anuncios = relationship("Anuncio", back_populates="usuario")
    Anuncio.usuario = relationship("Usuario", back_populates="anuncios")
    Usuario.lotes = relationship("Lote", back_populates="usuario")
    Lote.usuario = relationship("Usuario", back_populates="lotes")
    Bloco.lote_blocos = relationship("LoteBlocos", back_populates="bloco")
    LoteBlocos.bloco = relationship("Bloco", back_populates="lote_blocos")
    Lote.lote_blocos = relationship("LoteBlocos", back_populates="lote")
    LoteBlocos.lote = relationship("Lote", back_populates="lote_blocos")
    
    # Relacionamentos do Chat - CORRIGIDOS
    # Relacionamentos da Conversa
    Conversa.usuario1 = relationship("Usuario", foreign_keys=[Conversa.usuario1_id])
    Conversa.usuario2 = relationship("Usuario", foreign_keys=[Conversa.usuario2_id])
    Conversa.bloco = relationship("Bloco", foreign_keys=[Conversa.bloco_id])
    Conversa.mensagens = relationship("Mensagem", back_populates="conversa", cascade="all, delete-orphan")
    
    # Relacionamentos da Mensagem
    Mensagem.conversa = relationship("Conversa", back_populates="mensagens")
    Mensagem.usuario = relationship("Usuario", foreign_keys=[Mensagem.usuario_id])
    
    # Relacionamentos reversos para Usuario
    Usuario.conversas_usuario1 = relationship("Conversa", foreign_keys=[Conversa.usuario1_id])
    Usuario.conversas_usuario2 = relationship("Conversa", foreign_keys=[Conversa.usuario2_id]) 
    Usuario.mensagens = relationship("Mensagem", foreign_keys=[Mensagem.usuario_id])

# Criar as tabelas no banco de dados
def init_db():
    define_relationships()
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()