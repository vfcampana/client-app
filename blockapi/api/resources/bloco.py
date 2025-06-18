from flask import jsonify, request
from flask_restful import Resource
from sqlalchemy.orm import sessionmaker
from models.bloco import Bloco
from models.extensions import engine, verificar_jwt
from datetime import datetime
import requests

Session = sessionmaker(bind=engine)

session = Session()


class BlocoPublic(Resource):
    def get(self):
        """Endpoint público para mostrar todos os blocos na Home"""
        session = Session()
        try:
            blocos = session.query(Bloco).filter(Bloco.status == "1").all()
            
            lista_blocos = []
            for bloco in blocos:
                lista_blocos.append(bloco.to_dict())
            
            return lista_blocos, 200 
            
        except Exception as e:
            return {"message": "Erro ao buscar blocos", "error": str(e)}, 500
        finally:
            session.close()

class BlocoList(Resource):
    def get(self):

        id_usuario = verificar_jwt()
        if id_usuario['code'] != 200 or not id_usuario.get('message'):
            response = jsonify({"message": id_usuario.get('message', 'Token inválido ou não fornecido')})
            response.status_code = id_usuario['code'] # type: ignore
            return response
        
        blocos = session.query(Bloco).filter(Bloco.id_usuario == id_usuario['message']).all()
        lista_blocos = []

        for bloco in blocos:
            lista_blocos.append(bloco.to_dict())

        response = jsonify(lista_blocos)
        response.status_code = 200
        return response

class BlocoGet(Resource):
    def get(self, id):

        id_usuario = verificar_jwt()

        if id_usuario['code'] != 200:
            response = jsonify({"message": id_usuario['message']})
            response.status_code = id_usuario['code'] # type: ignore
            return response

        bloco = session.query(Bloco).filter(Bloco.id == id).first()

        if not bloco:
            response = jsonify({"message": "Bloco não encontrado"})
            response.status_code = 404
            return response
        
        response = jsonify(bloco.to_dict())
        response.status_code = 200
        return response
    
class BlocoDelete(Resource):
    def delete(self, id):
        id_usuario = verificar_jwt()
        
        if id_usuario['code'] != 200:
            respose = jsonify({"message": id_usuario['message']})
            respose.status_code = id_usuario['code'] # type: ignore
            return respose
        
        bloco = session.query(Bloco).filter(Bloco.id == id).filter(Bloco.id_usuario == id_usuario['message']).first()
        
        if not bloco:
            response = jsonify({"message": "Bloco não encontrado"})
            response.status_code = 404
            return response
        
        session.delete(bloco)
        session.commit()
        
        response = jsonify({"message": "Bloco deletado com sucesso"})
        response.status_code = 200
        return response
    
class BlocoAtualiza(Resource):
    def put(self, id):
        id_usuario = verificar_jwt()

        if id_usuario['code'] != 200:
            response = jsonify({"message": id_usuario['message']})
            response.status_code = id_usuario['code']
            return response
        
        data = request.get_json()
        
        bloco = session.query(Bloco).filter(Bloco.id == id).first()

        if not bloco:
            response = jsonify({"message": "Bloco não encontrado"})
            response.status_code = 404
            return response

        bloco.titulo = data.get("titulo", bloco.titulo)
        bloco.classificacao = data.get("classificacao", bloco.classificacao)
        bloco.coloracao = data.get("coloracao", bloco.coloracao)
        bloco.material = data.get("material", bloco.material)
        bloco.medida_bruta = data.get("medida_bruta", bloco.medida_bruta)
        bloco.volume_bruto = data.get("volume_bruto", bloco.volume_bruto)
        bloco.medida_liquida = data.get("medida_liquida", bloco.medida_liquida)
        bloco.volume_liquido = data.get("volume_liquido", bloco.volume_liquido)
        bloco.pedreira = data.get("pedreira", bloco.pedreira)
        bloco.observacoes = data.get("observacoes", bloco.observacoes)
        if data.get("cep"):
            bloco.cep = data['cep']
            res = requests.get(f"https://viacep.com.br/ws/{bloco.cep}/json/")
            bloco.logradouro = str(res.json()['logradouro']) + ', ' + str(res.json()['bairro'])
            bloco.cidade = res.json()['localidade']
            bloco.estado = res.json()['uf']
            bloco.pais = 'Brasil'

        bloco.valor = data.get("valor", bloco.valor)
        bloco.status = data.get("status", bloco.status)
            
        
        session.commit()
        session.close()

        response = jsonify({"message": "Bloco atualizado com sucesso"})
        response.status_code = 200
        return response

class BlocoCadastro(Resource):
    
    def post(self):
        id_usuario = verificar_jwt()
        
        if id_usuario['code'] != 200:
            respose = jsonify({"message": id_usuario['message']})
            respose.status_code = id_usuario['code']
            return respose

        data = request.get_json()

        titulo = data.get("titulo")
        classificacao = data.get("classificacao")
        coloracao = data.get("coloracao")
        material = data.get("material")
        medida_bruta = data.get("medida_bruta")
        volume_bruto = data.get("volume_bruto")
        medida_liquida = data.get("medida_liquida")
        volume_liquido = data.get("volume_liquido")
        pedreira = data.get("pedreira")
        observacoes = data.get("observacoes")
        cep = data.get("cep")
        if cep:
            res = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
            logradouro = str(res.json()['logradouro']) + ', ' + str(res.json()['bairro'])
            cidade = res.json()['localidade']
            estado = res.json()['uf']
            pais = 'Brasil'
        valor = data.get("valor")
        data_criacao = datetime.now()
        data_alteracao = datetime.now()
        status = str(data.get("status"))
        
        if titulo and classificacao and coloracao and material and medida_bruta and volume_bruto and medida_liquida and volume_liquido and pedreira and observacoes and cep and logradouro and pais and cidade and valor and data_criacao and data_alteracao and estado and id_usuario and status:
            
            bloco = Bloco(
                titulo=titulo,
                classificacao=classificacao,
                coloracao=coloracao,
                material=material,
                medida_bruta=medida_bruta,
                volume_bruto=volume_bruto,
                medida_liquida=medida_liquida,
                volume_liquido=volume_liquido,
                pedreira=pedreira,
                observacoes=observacoes,
                cep=cep,
                logradouro=logradouro,
                pais=pais,
                cidade=cidade,
                valor=valor,
                data_criacao=data_criacao,
                data_alteracao=data_alteracao,
                estado=estado,
                id_usuario=str(id_usuario['message']),
                status=status
            )
            session.add(bloco)
            session.commit()
            session.close()

            response = jsonify({"message": "Bloco cadastrado com sucesso"})
            return response
        
        else:
            response = jsonify({"message": "Dados inválidos"})
            response.status_code = 401
            return response