from flask import jsonify
from flask_restful import Resource
from flask import jsonify, request
from flask_restful import Resource
from sqlalchemy.orm import sessionmaker
from models.bloco import Bloco
from models.lote import Lote
from models.lote_bloco import LoteBlocos
from models.extensions import engine, verificar_jwt

Session = sessionmaker(bind=engine)

session = Session()

class LoteList(Resource):
    def get(self):
        
        print("Listando lotes")
        id_usuario = verificar_jwt()

        if id_usuario['code'] != 200:
            response = jsonify({"message": id_usuario['message']})
            response.status_code = id_usuario['code']
            return response
        
        lotes = session.query(Lote).filter(Lote.id_usuario == id_usuario['message']).all()

        lista_lotes = []

        for lote in lotes:
            lote_dict = lote.to_dict()
            lote_dict['blocos'] = []

            lote_blocos = session.query(LoteBlocos).filter(LoteBlocos.id_lote == lote.id).all()
            for lote_bloco in lote_blocos:
                lote_dict['blocos'].append(lote_bloco.id_bloco)

            lista_lotes.append(lote_dict)

        print("Lotes encontrados:", lista_lotes)

        response = jsonify(lista_lotes)
        response.status_code = 200
        return response

class LoteGet(Resource):
    def get(self, id):
        
        print("Obtendo lote")
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

class LoteDelete(Resource):
    def delete(self, id):
        id_usuario = verificar_jwt()
        
        if id_usuario['code'] != 200:
            respose = jsonify({"message": id_usuario['message']})
            respose.status_code = id_usuario['code']
            return respose
        
        
        lote = session.query(Lote).filter(Lote.id == id).filter(Lote.id_usuario == id_usuario['message']).first()
        
        if not lote:
            response = jsonify({"message": "Lote não encontrado"})
            response.status_code = 404
            return response
        
        lote_blocos = session.query(LoteBlocos).filter(LoteBlocos.id_lote == id).all()
        
        for lote_bloco in lote_blocos:
            session.delete(lote_bloco)
            session.commit()
        
        session.delete(lote)
        session.commit()
        
        response = jsonify({"message": "Lote deletado com sucesso"})
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

        if 'status' in data:
            data['status'] = 0 if data['status'] == 'privado' else 1

        print(data)
        lote = session.query(Lote).filter(Lote.id == id).filter(Lote.id_usuario == id_usuario['message']).first()

        if not lote:
            response = jsonify({"message": "Lote não encontrado"})
            response.status_code = 404
            return response
        
        lote.nome = data.get('nome', lote.nome)
        lote.preco = data.get('preco', lote.preco)
        lote.observacoes = data.get('observacoes', lote.observacoes)
        lote.status = data.get('status', lote.status)

        session.add(lote)
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
                if str(bloco.id_usuario) != str(id_usuario['message']):
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


class LoteCadastro(Resource):
    def post(self):
        print("Cadastrando lote")
        id_usuario = verificar_jwt()

        if id_usuario['code'] != 200:
            response = jsonify({"message": id_usuario['message']})
            response.status_code = id_usuario['code']
            return response

        data = request.get_json()
        nome = data.get('nome')
        preco = data.get('preco')
        observacoes = data.get('observacoes')
        blocos = data.get('blocos')
        status = data.get('status')
        
        if nome and preco and observacoes and status and blocos:

            status = 0 if status == 'privado' else 1
            for bloco in blocos:
                bloco = session.query(Bloco).filter(Bloco.id == bloco).first()
                if not bloco:
                    response = jsonify({"message": "Bloco não encontrado"})
                    response.status_code = 404
                    return response
                if str(bloco.id_usuario) != id_usuario['message']:
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