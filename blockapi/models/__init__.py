from sqlalchemy.orm import declarative_base
from ..extensions import engine

Base = declarative_base()

from sqlalchemy.orm import relationship
from .bloco import Bloco
from .usuario import Usuario
from .imagem import Imagens
from .anuncio import Anuncio
from .lote_bloco import LoteBlocos
from .chat import Chat
from .mensagem import Mensagens


def define_relationships():
    Bloco.usuario = relationship("Usuario", back_populates="blocos")
    Imagens.bloco = relationship("Bloco", back_populates="imagens")
    Anuncio.usuario = relationship("Usuario", back_populates="anuncios")
    LoteBlocos.bloco = relationship("Bloco", back_populates="lote_blocos")
    LoteBlocos.lote = relationship("Lote", back_populates="lote_blocos")
    Chat.anuncio = relationship("Anuncio", back_populates="chats")
    Chat.cliente = relationship("Usuario", back_populates="chats")
    Mensagens.chat = relationship("Chat", back_populates="mensagens")
    Mensagens.remetente = relationship("Usuario", back_populates="mensagens")
    
define_relationships()

Base.metadata.create_all(engine)






