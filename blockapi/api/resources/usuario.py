from flask import jsonify, request
from flask_restful import Resource
from sqlalchemy.orm import sessionmaker
from models.usuario import Usuario
from models.extensions import engine
from datetime import datetime
from flask_login import login_user

Session = sessionmaker(bind=engine)
session = Session()

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

        if user and user.senha == senha:
            login_user(user)
            return jsonify({"message": "Login realizado com sucesso"})
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
            response.status_code = 401
            return response

class UsuarioAtualiza(Resource):
    def put(self):
        return jsonify({'login': 'login'})