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
    def get(self, id ):
        
        id_usuario = id
        
        verificar = verificar_jwt()
        
        if verificar['code'] != 200:
            response = jsonify({"message": verificar['message']})
            response.status_code = verificar['code']
            return response
        
        if not id_usuario:
            response = jsonify({"message": "ID do usuário não fornecido"})
            response.status_code = 400
            return response
        
        user = session.query(Usuario).filter(Usuario.id == id_usuario).first()

        if user:
            response = jsonify(
            id=user.id,
            nome=user.nome,
            documento=user.documento,
            email=user.email,
            telefone=user.telefone,
            cep=user.cep,
            logradouro=user.logradouro,
            cidade=user.cidade,
            pais=user.pais,
            data_registro=user.data_registro,
            estado=user.estado
            )
            response.status_code = 200
            return response
        else:
            response = jsonify({"message": "Usuário não encontrado"})
            response.status_code = 404
            return response

class UsuarioDelete(Resource):
    def delete(self):
        id_usuario = verificar_jwt()
        
        if id_usuario['code'] != 200:
            respose = jsonify({"message": id_usuario['message']})
            respose.status_code = id_usuario['code']
            return respose
        
        usuario = session.query(Usuario).filter(Usuario.id == id_usuario['message']).first()
        
        if not usuario:
            response = jsonify({"message": "Conta não encontrada"})
            response.status_code = 404
            return response
        
        session.delete(usuario)
        session.commit()
        
        response = jsonify({"message": "Conta deletada com sucesso"})
        response.status_code = 200
        return response

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
        if cep:
            res = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
            logradouro = str(res.json()['logradouro']) + ', ' + str(res.json()['bairro'])
            cidade = res.json()['localidade']
            estado = res.json()['uf']
            pais = 'Brasil'
        senha = data.get("senha")

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

                user = session.query(Usuario).filter(Usuario.email == email).first()

                access_token = create_access_token(identity=user.id)
                response =  jsonify(access_token=access_token)
                response.status_code = 200
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
    def put(self):
        id_usuario = verificar_jwt()
        
        if id_usuario['code'] != 200:
            respose = jsonify({"message": id_usuario['message']})
            respose.status_code = id_usuario['code']
            return respose
        
        user = session.query(Usuario).filter(Usuario.id == id_usuario['message']).first()

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
