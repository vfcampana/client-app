from flask import Blueprint
from flask_restful import Api
from api.resources.usuario import UsuarioGet, UsuarioAtualiza, UsuarioLogin, UsuarioCadastro, UsuarioProtected
from api.resources.bloco import BlocoList, BlocoGet, BlocoAtualiza, BlocoCadastro
from api.resources.anuncio import AnuncioList, AnuncioGet, AnuncioAtualiza, AnuncioCadastro
from api.resources.lote import LoteList, LoteGet, LoteAtualiza, LoteCadastro
from api.resources.chat import ChatList, ChatGet, EnviarMensagem

api_bp = Blueprint('api', __name__)

api = Api(api_bp)


# Rotas de Usuário / Autenticação

api.add_resource(UsuarioGet, '/usuario/<int:id>')
api.add_resource(UsuarioAtualiza, '/usuario')
api.add_resource(UsuarioLogin, '/login')
api.add_resource(UsuarioCadastro, '/cadastro')
api.add_resource(UsuarioProtected, '/protected')


# Rotas de Blocos

api.add_resource(BlocoList, '/bloco')
api.add_resource(BlocoGet, '/bloco/<int:id>')
api.add_resource(BlocoAtualiza, '/bloco/<int:id>')
api.add_resource(BlocoCadastro, '/bloco')


# Rotas de Anuncios

api.add_resource(AnuncioList, '/anuncio')
api.add_resource(AnuncioGet, '/anuncio/<int:id>')
api.add_resource(AnuncioAtualiza, '/anuncio/<int:id>')
api.add_resource(AnuncioCadastro, '/anuncio')


# Rotas de Lotes / Lote_Blocos

api.add_resource(LoteList, '/lote')
api.add_resource(LoteGet, '/lote/<int:id>')
api.add_resource(LoteAtualiza, '/lote/<int:id>')
api.add_resource(LoteCadastro, '/lote')


# Rotas de Chat / Mensagens

api.add_resource(ChatList, '/chat')
api.add_resource(ChatGet, '/chat/<int:id>')

api.add_resource(EnviarMensagem, '/chat/<int:id>')
