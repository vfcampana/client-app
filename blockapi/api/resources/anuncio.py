from flask import jsonify, request
from flask_restful import Resource
from models.extensions import engine, verificar_jwt
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models.anuncio import Anuncio
from models.bloco import Bloco
from models.lote import Lote

Session = sessionmaker(bind=engine)

session = Session()

class AnuncioList(Resource):
    def get(self):
        
        anuncios = session.query(Anuncio).all()

        response = jsonify(anuncios)
        response.status_code = 200
        return response

class AnuncioGet(Resource):
    def get(self, id):

        anuncio = session.query(Anuncio).filter(Anuncio.id == id).first()

        if not anuncio:
            response = jsonify({"message": "Anuncio não encontrado"})
            response.status_code = 404
            return response
        
        response = jsonify(anuncio.to_dict())
        response.status_code = 200
        return response

class AnuncioDelete(Resource):
    def delete(self, id):
        id_usuario = verificar_jwt()
        
        if id_usuario['code'] != 200:
            response = jsonify({"message": id_usuario['message']})
            response.status_code = int(id_usuario['code'])
            return response
        
        anuncio = session.query(Anuncio).filter(Anuncio.id == id).filter(Anuncio.id_usuario == id_usuario['message']).first()
        
        if not anuncio:
            response = jsonify({"message": "Anuncio não encontrado"})
            response.status_code = 404
            return response
        
        session.delete(anuncio)
        session.commit()
        
        response = jsonify({"message": "Anuncio deletado com sucesso"})
        response.status_code = 200
        return response

class AnuncioCadastro(Resource):
    def post(self):
        id_usuario = verificar_jwt()
        
        if id_usuario['code'] != 200:
            respose = jsonify({"message": id_usuario['message']})
            respose.status_code = id_usuario['code']
            return respose

        data = request.get_json()

        id_bloco = data.get("id_bloco")
        id_lote = data.get("id_lote")
        id_usuario = id_usuario['message']
        data_criacao = datetime.now()
        data_alteracao = datetime.now()
        status = 1
        
        verificarBlocoExistente = session.query(Bloco).filter(Bloco.id == id_bloco).filter(Bloco.status== '1').filter(Bloco.id_usuario==id_usuario).first()
        
        verificarLoteExistente = session.query(Lote).filter(Lote.id == id_lote).filter(Lote.status== '1').filter(Lote.id_usuario==id_usuario).first()

            
        if id_bloco and not id_lote:
            
            if not verificarBlocoExistente:
                response = jsonify({"message": "Bloco não encontrado ou não pertence ao usuário"})
                response.status_code = 404
                return response
        
            anuncio = Anuncio(
                id_bloco=id_bloco,
                id_usuario=id_usuario,
                data_criacao=data_criacao,
                data_alteracao=data_alteracao,
                status=status
            )
            
        elif id_bloco and id_lote:
            
            if not verificarBlocoExistente:
                response = jsonify({"message": "Bloco não encontrado ou não pertence ao usuário"})
                response.status_code = 404
                return response
        
            if not verificarLoteExistente:
                response = jsonify({"message": "Lote não encontrado ou não pertence ao usuário"})
                response.status_code = 404
                return response

            anuncio = Anuncio(
                id_bloco=id_bloco,
                id_lote=id_lote,
                id_usuario=id_usuario,
                data_criacao=data_criacao,
                data_alteracao=data_alteracao,
                status=status
            )
            
        elif not id_bloco and id_lote:
            
            if not verificarLoteExistente:
                response = jsonify({"message": "Lote não encontrado ou não pertence ao usuário"})
                response.status_code = 404
                return response
            
            anuncio = Anuncio(
                id_lote=id_lote,
                id_usuario=id_usuario,
                data_criacao=data_criacao,
                data_alteracao=data_alteracao,
                status=status
            )
            
        session.add(anuncio)
        session.commit()
        session.close()

        response = jsonify({"message": "Anuncio criado com sucesso"})
        return response