from sqlalchemy.orm import relationship
from models.extensions import engine
from models.base import Base
from bloco import Bloco
from usuario import Usuario
from imagem import Imagens
from anuncio import Anuncio
from lote_bloco import LoteBlocos
from lote import Lote
from mensagem import Mensagem
from conversa import Conversa

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