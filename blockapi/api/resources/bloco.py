from flask import jsonify, request
from flask_restful import Resource
from sqlalchemy.orm import sessionmaker
from models.bloco import Bloco
from models.extensions import engine, verificar_jwt
from datetime import datetime

Session = sessionmaker(bind=engine)

session = Session()

class BlocoList(Resource):
    def get(self):
        return jsonify({'bloco': 'bloco'})

class BlocoGet(Resource):
    def get(self):
        return jsonify({'bloco': 'bloco'})

class BlocoAtualiza(Resource):
    def put(self):
        return jsonify({'bloco': 'bloco'})

class BlocoCadastro(Resource):
    
    def post(self):
        
        id_usuario = verificar_jwt()

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
        logradouro = data.get("logradouro")
        pais = data.get("pais")
        cidade = data.get("cidade")
        valor = data.get("valor")
        data_criacao = datetime.now()
        data_alteracao = datetime.now()
        estado = data.get("estado")
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
                id_usuario=str(id_usuario),
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