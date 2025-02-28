from flask import jsonify, request
from flask_restful import Resource
from sqlalchemy.orm import sessionmaker
from models.usuario import Usuario
from models.extensions import engine, verificar_jwt
from datetime import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import requests

Session = sessionmaker(bind=engine)
session = Session()

class UsuarioProtected(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        return jsonify(logged_in_as=current_user_id)
    
class UsuarioGet(Resource):
    def get(self):
        return jsonify({'usuario': 'usuario'})

class UsuarioList(Resource):
    def get(self):
        return jsonify({'usuario': 'usuario'})

class UsuarioLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        senha = data.get("senha")

        user = session.query(Usuario).filter(Usuario.email == email).first()

        if user and user.verificar_senha(str(senha)):
            access_token = create_access_token(identity=user.id)
            response =  jsonify(access_token=access_token)
            response.status_code = 200
            return response
        else:
            response = jsonify({"message": "Credenciais inválidas"})
            response.status_code = 401
            return response

class UsuarioCadastro(Resource):
    def post(self):
        data = request.get_json()
        nome = data.get("nome")
        documento = data.get("documento")
        email = data.get("email")
        telefone = data.get("telefone")
        cep = data.get("cep")
        logradouro = data.get("logradouro")
        cidade = data.get("cidade")
        pais = data.get("pais")
        senha = data.get("senha")
        estado = data.get("estado")

        if nome and documento and email and telefone and cep and logradouro and cidade and pais and senha and estado:
            db_user = session.query(Usuario).filter(Usuario.email == email).first()

            if not db_user:
                user = Usuario(
                    nome=nome,
                    documento=documento,
                    email=email,
                    telefone=telefone,
                    cep=cep,
                    logradouro=logradouro,
                    cidade=cidade,
                    pais=pais,
                    senha=senha,
                    data_registro=datetime.now(),
                    estado=estado
                )
                
                user.set_senha(senha)
                
                session.add(user)
                session.commit()
                session.close()

                response = jsonify({"message": "Usuário cadastrado com sucesso"})
                return response
            else:
                response = jsonify({"message": "Usuário já cadastrado"})
                response.status_code = 409
                return response
        else:
            response = jsonify({"message": "Dados inválidos"})
            response.status_code = 400
            return response

class UsuarioAtualiza(Resource):
    def put(self, id):
        user_id = verificar_jwt()
        print(user_id)
        user = session.query(Usuario).filter(Usuario.id == user_id).first()

        if user:
            data = request.get_json()
            if data.get('nome'):
                user.nome = data['nome']
            if data.get('telefone'):
                user.telefone = data['telefone']
            if data.get('cep'):
                user.cep = data['cep']
                res = requests.get(f'https://viacep.com.br/ws/{user.cep}/json/')
                user.logradouro = str(res.json()['logradouro']) + ', ' + str(res.json()['bairro'])
                user.cidade = res.json()['localidade']
                user.estado = res.json()['uf']
                user.pais = 'Brasil'

            session.commit()
            session.close()

            response = jsonify({'message': 'Dados atualizados com sucesso'})
            response.status_code = 200
            return response
        else:
            response = jsonify({"message": "Usuário não encontrado"})
            response.status_code = 404
            return response
