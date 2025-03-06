from flask import jsonify
from flask_restful import Resource
from flask import jsonify, request
from flask_restful import Resource
from sqlalchemy.orm import sessionmaker
from models.bloco import Bloco
from models.lote import Lote
from models.lote_bloco import LoteBlocos
from models.extensions import engine, verificar_jwt
from datetime import datetime
import requests

Session = sessionmaker(bind=engine)

session = Session()

class LoteList(Resource):
    def get(self):
        
        id_usuario = verificar_jwt()

        if id_usuario['code'] != 200:
            response = jsonify({"message": id_usuario['message']})
            response.status_code = id_usuario['code']
            return response
        
        lotes = session.query(Lote).filter(Lote.id_usuario == id_usuario['message']).all()

        lista_lotes = []

        for lote in lotes:
            lista_lotes.append(lote.to_dict())

        response = jsonify(lista_lotes)
        response.status_code = 200
        return response

class LoteGet(Resource):
    def get(self):
        return jsonify({'lote': 'lote'})

class LoteAtualiza(Resource):
    def put(self):
        return jsonify({'lote': 'lote'})

class LoteCadastro(Resource):
    def post(self):

        id_usuario = verificar_jwt()

        if id_usuario['code'] != 200:
            response = jsonify({"message": id_usuario['message']})
            response.status_code = id_usuario['code']
            return response

        data = request.get_json()
        nome = data.get('nome')
        preco = data.get('preco')
        observacoes = data.get('observacoes')
        status = data.get('status')
        blocos = data.get('blocos')
        
        if nome and preco and observacoes and status and blocos:

            for bloco in blocos:
                bloco = session.query(Bloco).filter(Bloco.id == bloco).first()
                if not bloco:
                    response = jsonify({"message": "Bloco não encontrado"})
                    response.status_code = 404
                    return response
                if bloco.id_usuario != id_usuario['message']:
                    response = jsonify({"message": "Bloco não pertence ao usuário"})	
                    response.status_code = 404
                    return response

            lote = Lote(
                nome=nome, 
                preco=preco, 
                observacoes=observacoes, 
                id_usuario=str(id_usuario['message']),
                status=status
            )

            session.add(lote)
            session.commit()
            
            for bloco in blocos:

                lote_blocos = LoteBlocos(
                    id_bloco=bloco,
                    id_lote=lote.id
                )
                session.add(lote_blocos)

            session.commit()
            session.close()

            response = jsonify({"message": "Lote cadastrado com sucesso"})
            response.status_code = 201
            return response
        
        else:
            response = jsonify({"message": "Dados inválidos"})
            response.status_code = 401
            return response