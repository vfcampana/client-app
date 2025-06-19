from flask import Blueprint
from flask_restful import Api
from api.resources.usuario import UsuarioGet, UsuarioAtualiza, UsuarioDelete, UsuarioLogin, UsuarioCadastro, UsuarioProtected
from api.resources.bloco import BlocoPublic, BlocoList, BlocoGet, BlocoDelete, BlocoAtualiza, BlocoCadastro
from api.resources.anuncio import AnuncioList, AnuncioGet, AnuncioDelete, AnuncioCadastro
from api.resources.lote import LoteList, LoteGet, LoteDelete, LoteAtualiza, LoteCadastro
from api.resources.chat import ChatList, ChatGet, EnviarMensagem
from api.resources.favorito import FavoritoPost, FavoritoGet, FavoritoDelete

api_bp = Blueprint('api', __name__)

api = Api(api_bp)


# Rotas de Usuário / Autenticação

api.add_resource(UsuarioGet, '/usuario/<int:id>')
api.add_resource(UsuarioAtualiza, '/usuario')
api.add_resource(UsuarioDelete, '/usuario')
api.add_resource(UsuarioLogin, '/login')
api.add_resource(UsuarioCadastro, '/cadastro')
api.add_resource(UsuarioProtected, '/protected')


# Rotas de Blocos

api.add_resource(BlocoPublic, '/bloco')
api.add_resource(BlocoList, '/blocos')
api.add_resource(BlocoGet, '/bloco/<int:id>')
api.add_resource(BlocoDelete, '/bloco/<int:id>')
api.add_resource(BlocoAtualiza, '/bloco/<int:id>')
api.add_resource(BlocoCadastro, '/bloco')

# Rotas de Favoritos
api.add_resource(FavoritoPost, '/favorito')
api.add_resource(FavoritoGet, '/favorito')
api.add_resource(FavoritoDelete, '/favorito/<int:id>')


# Rotas de Anuncios

api.add_resource(AnuncioList, '/anuncio')
api.add_resource(AnuncioGet, '/anuncio/<int:id>')
api.add_resource(AnuncioDelete, '/anuncio/<int:id>')
api.add_resource(AnuncioCadastro, '/anuncio')


# Rotas de Lotes / Lote_Blocos

api.add_resource(LoteList, '/lote')
api.add_resource(LoteGet, '/lote/<int:id>')
api.add_resource(LoteDelete, '/lote/<int:id>')
api.add_resource(LoteAtualiza, '/lote/<int:id>')
api.add_resource(LoteCadastro, '/lote')


# Rotas de Chat / Mensagens

api.add_resource(ChatList, '/chat')
api.add_resource(ChatGet, '/chat/<int:id>')

api.add_resource(EnviarMensagem, '/chat/<int:id>')
