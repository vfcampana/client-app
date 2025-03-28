from flask import jsonify
from flask_restful import Resource
from models.extensions import engine, verificar_jwt
from sqlalchemy.orm import sessionmaker
from models.anuncio import Anuncio

Session = sessionmaker(bind=engine)

session = Session()

class AnuncioList(Resource):
    def get(self):

        id_usuario = verificar_jwt()

        if id_usuario['code'] != 200:
            response = jsonify({"message": id_usuario['message']})
            response.status_code = id_usuario['code']
            return response
        
        anuncios = session.query(Anuncio).all()

        response = jsonify(anuncios)
        response.status_code = 200
        return response

class AnuncioGet(Resource):
    def get(self, id):

        id_usuario = verificar_jwt()

        if id_usuario['code'] != 200:
            response = jsonify({"message": id_usuario['message']})
            response.status_code = id_usuario['code']
            return response

        anuncio = session.query(Anuncio).filter(Anuncio.id == id).first()

        if not anuncio:
            response = jsonify({"message": "Anuncio não encontrado"})
            response.status_code = 404
            return response
        
        response = jsonify(anuncio.to_dict())
        response.status_code = 200
        return response

class AnuncioAtualiza(Resource):
    def put(self):
        return jsonify({'anuncio': 'anuncio'})

class AnuncioCadastro(Resource):
    def post(self):
        return jsonify({'anuncio': 'anuncio'})
