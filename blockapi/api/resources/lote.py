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
    def get(self, id):
        
        id_usuario = verificar_jwt()

        if id_usuario['code'] != 200:
            response = jsonify({"message": id_usuario['message']})
            response.status_code = id_usuario['code']
            return response

        lote = session.query(Lote).filter(Lote.id == id).first()

        if not lote:
            response = jsonify({"message": "Lote não encontrado"})
            response.status_code = 404
            return response
        
        lote_json = lote.to_dict()

        lote_json['blocos'] = []

        lista_lote_blocos = session.query(LoteBlocos).filter(LoteBlocos.id_lote == id).all()
        
        for lote_bloco in lista_lote_blocos:
            bloco = session.query(Bloco).filter(Bloco.id == lote_bloco.id_bloco).first()
            if bloco:
                lote_json['blocos'].append(bloco.to_dict())        
        
        response = jsonify(lote_json)
        response.status_code = 200
        return response

class LoteAtualiza(Resource):
    def put(self, id):

        id_usuario = verificar_jwt()

        if id_usuario['code'] != 200:
            response = jsonify({"message": id_usuario['message']})
            response.status_code = id_usuario['code']
            return response
        
        data = request.get_json()

        lote = session.query(Lote).filter(Lote.id == id).filter(Lote.id_usuario == id_usuario['message']).first()

        if not lote:
            response = jsonify({"message": "Lote não encontrado"})
            response.status_code = 404
            return response
        
        lote.nome = data.get('nome', lote.nome)
        lote.preco = data.get('preco', lote.preco)
        lote.observacoes = data.get('observacoes', lote.observacoes)
        lote.status = data.get('status', lote.status)

        if data.get('blocos'):
            lote_bloco = session.query(LoteBlocos).filter(LoteBlocos.id_lote == id).all()
            
            for lote_bloco in lote_bloco:
                session.delete(lote_bloco)

            for bloco in data.get('blocos'):
                bloco = session.query(Bloco).filter(Bloco.id == bloco).first()
                if not bloco:
                    response = jsonify({"message": "Bloco não encontrado"})
                    response.status_code = 404
                    return response
                if bloco.id_usuario != id_usuario['message']:
                    response = jsonify({"message": "Bloco não pertence ao usuário"})	
                    response.status_code = 404
                    return response
                
                lote_blocos = LoteBlocos(
                    id_bloco=bloco.id,
                    id_lote=lote.id
                )
                session.add(lote_blocos)

            session.commit()
            session.close()

            response = jsonify({"message": "Lote atualizado com sucesso"})
            response.status_code = 200
            return response
        
                

                

                

        session.commit()
        session.close()

        response = jsonify({"message": "Lote atualizado com sucesso"})
        response.status_code = 200
        return response
        


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