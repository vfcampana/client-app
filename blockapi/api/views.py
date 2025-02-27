from flask import Blueprint
from flask_restful import Api
from api.resources.usuario import UsuarioList, UsuarioGet, UsuarioAtualiza, UsuarioLogin, UsuarioCadastro

api_bp = Blueprint('api', __name__)

api = Api(api_bp)

api.add_resource(UsuarioList, '/usuario')
api.add_resource(UsuarioGet, '/usuario/<int:id>')
api.add_resource(UsuarioAtualiza, '/usuario/<int:id>')
api.add_resource(UsuarioLogin, '/login')
api.add_resource(UsuarioCadastro, '/cadastro')