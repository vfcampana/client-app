from flask import request
from flask_restful import Resource
from sqlalchemy.orm import sessionmaker
from models.bloco import Bloco
from models.favorito import Favorito
from models.extensions import engine, verificar_jwt

Session = sessionmaker(bind=engine)

class FavoritoGet(Resource):
    def get(self):
        """Endpoint para listar os blocos favoritos de um usuário"""
        session = Session()
        try:
            id_usuario = verificar_jwt()
            if id_usuario['code'] != 200 or not id_usuario.get('message'):
                return {"message": id_usuario.get('message', 'Token inválido ou não fornecido')}, id_usuario['code']
            
            favoritos = session.query(Favorito).filter_by(id_usuario=id_usuario['message']).all()
            if not favoritos:
                return {"message": "Nenhum bloco favorito encontrado"}, 404
            
            blocos_favoritos = []
            for favorito in favoritos:
                bloco = session.query(Bloco).filter_by(id=favorito.id_bloco).first()
                if bloco:
                    blocos_favoritos.append(bloco.to_dict())
            
            return blocos_favoritos, 200
        finally:
            session.close()

class FavoritoDelete(Resource):
    def delete(self, id):
        """Endpoint para remover um bloco dos favoritos de um usuário"""
        session = Session()
        try:
            id_usuario = verificar_jwt()
            if id_usuario['code'] != 200 or not id_usuario.get('message'):
                return {"message": id_usuario.get('message', 'Token inválido ou não fornecido')}, id_usuario['code']

            if id is None:
                return {"message": "ID do bloco é obrigatório"}, 400

            favorito = session.query(Favorito).filter(
                Favorito.id_bloco == id,
                Favorito.id_usuario == id_usuario['message']
            ).first()

            if favorito:
                session.delete(favorito)
                session.commit()
                return {"message": "Bloco removido dos favoritos com sucesso"}, 200
            else:
                return {"message": "Bloco não encontrado nos favoritos"}, 404
        finally:
            session.close()

class FavoritoPost(Resource):
    def post(self):
        """Endpoint para adicionar um bloco aos favoritos de um usuário"""
        session = Session()
        try:
            id_usuario = verificar_jwt()
            if id_usuario['code'] != 200 or not id_usuario.get('message'):
                return {"message": id_usuario.get('message', 'Token inválido ou não fornecido')}, id_usuario['code']
            
            data = request.get_json()
            id_bloco = data.get('id_bloco')
            
            if not id_bloco:
                return {"message": "ID do bloco é obrigatório"}, 400
            
            bloco = session.query(Bloco).filter(Bloco.id == id_bloco).first()
            if not bloco:
                return {"message": "Bloco não encontrado"}, 404
            
            favorito_existente = session.query(Favorito).filter(
                Favorito.id_bloco == id_bloco,
                Favorito.id_usuario == id_usuario['message']
            ).first()
            
            if favorito_existente:
                return {"message": "Bloco já está nos favoritos"}, 400
            
            novo_favorito = Favorito(id_usuario=id_usuario['message'], id_bloco=id_bloco)
            session.add(novo_favorito)
            session.commit()
            
            return {"message": "Bloco adicionado aos favoritos com sucesso"}, 201
        finally:
            session.close()