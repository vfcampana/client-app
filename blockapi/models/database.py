from sqlalchemy.orm import relationship
from extensions import Base, engine
from bloco import Bloco
from usuario import Usuario
from imagem import Imagens
from anuncio import Anuncio
from lote_bloco import LoteBlocos
from lote import Lote
from chat import Chat
from mensagem import Mensagens

# Definição dos relacionamentos dentro de uma função
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

# Criar as tabelas no banco de dados
def init_db():
    define_relationships()
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
