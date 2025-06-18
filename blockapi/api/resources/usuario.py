from flask import jsonify, request
from flask_restful import Resource
from sqlalchemy.orm import sessionmaker
from models.usuario import Usuario
from models.extensions import engine, verificar_jwt
from datetime import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import requests

Session = sessionmaker(bind=engine)

class UsuarioProtected(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        return jsonify(logged_in_as=current_user_id)

class UsuarioCadastro(Resource):
    def post(self):
        session = Session()
        try:
            data = request.get_json()
            nome = data.get("nome")
            documento = data.get("documento")
            email = data.get("email")
            telefone = data.get("telefone")
            cep = data.get("cep")
            senha = data.get("senha")

            logradouro = ""
            cidade = ""
            estado = ""
            pais = "Brasil"

            if cep:
                try:
                    cep_limpo = cep.replace("-", "").replace(".", "").strip()
                    
                    if len(cep_limpo) != 8 or not cep_limpo.isdigit():
                        logradouro = "CEP com formato inválido"
                        cidade = "Cidade não informada"
                        estado = "Estado não informado"
                    else:
                        res = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/", timeout=10)
                        
                        if res.status_code == 200:
                            try:
                                cep_data = res.json()
                                
                                if not cep_data.get('erro'):
                                    logradouro_temp = cep_data.get('logradouro', '')
                                    bairro_temp = cep_data.get('bairro', '')
                                    
                                    if logradouro_temp and bairro_temp:
                                        logradouro = f"{logradouro_temp}, {bairro_temp}"
                                    elif logradouro_temp:
                                        logradouro = logradouro_temp
                                    elif bairro_temp:
                                        logradouro = bairro_temp
                                    else:
                                        logradouro = "Endereço não informado"
                                    
                                    cidade = cep_data.get('localidade', '')
                                    estado = cep_data.get('uf', '')
                                else:
                                    logradouro = "CEP não encontrado"
                                    cidade = "Cidade não informada"
                                    estado = "Estado não informado"
                            except ValueError:
                                logradouro = "Erro no formato da resposta"
                                cidade = "Cidade não informada"
                                estado = "Estado não informado"
                        else:
                            logradouro = "Erro ao consultar CEP"
                            cidade = "Cidade não informada"
                            estado = "Estado não informado"
                            
                except Exception as e:
                    logradouro = "Erro na consulta"
                    cidade = "Cidade não informada"
                    estado = "Estado não informado"

            if nome and documento and email and telefone and cep and senha:
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
                    session.refresh(user)

                    access_token = create_access_token(identity=str(user.id))
                    
                    response_data = {
                        "message": "Usuário cadastrado com sucesso",
                        "access_token": access_token,
                        "user": {
                            "id": user.id,
                            "nome": user.nome,
                            "email": user.email,
                            "documento": user.documento,
                            "telefone": user.telefone,
                            "cep": user.cep,
                            "logradouro": user.logradouro,
                            "cidade": user.cidade,
                            "estado": user.estado,
                            "pais": user.pais
                        }
                    }
                    
                    return response_data, 201
                    
                else:
                    return {"message": "Usuário já cadastrado"}, 409
            else:
                return {"message": "Dados obrigatórios não fornecidos"}, 400

        except Exception as e:
            session.rollback()
            return {"message": "Erro interno do servidor"}, 500
        
        finally:
            session.close()

class UsuarioLogin(Resource):
    def post(self):
        session = Session()
        try:
            data = request.get_json()
            email = data.get("email")
            senha = data.get("senha")

            user = session.query(Usuario).filter(Usuario.email == email).first()

            if user and user.verificar_senha(str(senha)):
                access_token = create_access_token(identity=str(user.id))
                return {
                    "access_token": access_token,
                    "user": {
                        "id": user.id,
                        "nome": user.nome,
                        "email": user.email
                    }
                }, 200
            else:
                return {"message": "Credenciais inválidas"}, 401
        finally:
            session.close()

class UsuarioGet(Resource):
    def get(self, id):
        session = Session()
        try:
            id_usuario = id
            verificar = verificar_jwt()
            
            if verificar['code'] != 200:
                return {"message": verificar['message']}, verificar['code']
            
            if not id_usuario:
                return {"message": "ID do usuário não fornecido"}, 400
            
            user = session.query(Usuario).filter(Usuario.id == id_usuario).first()

            if user:
                return {
                    "id": user.id,
                    "nome": user.nome,
                    "documento": user.documento,
                    "email": user.email,
                    "telefone": user.telefone,
                    "cep": user.cep,
                    "logradouro": user.logradouro,
                    "cidade": user.cidade,
                    "pais": user.pais,
                    "data_registro": user.data_registro.isoformat() if user.data_registro else None,
                    "estado": user.estado
                }, 200
            else:
                return {"message": "Usuário não encontrado"}, 404
        finally:
            session.close()

class UsuarioDelete(Resource):
    def delete(self):
        session = Session()
        try:
            id_usuario = verificar_jwt()
            
            if id_usuario['code'] != 200:
                return {"message": id_usuario['message']}, id_usuario['code']
            
            usuario = session.query(Usuario).filter(Usuario.id == id_usuario['message']).first()
            
            if not usuario:
                return {"message": "Conta não encontrada"}, 404
            
            session.delete(usuario)
            session.commit()
            
            return {"message": "Conta deletada com sucesso"}, 200
        finally:
            session.close()

class UsuarioAtualiza(Resource):
    def put(self):
        session = Session()
        try:
            id_usuario = verificar_jwt()
            
            if id_usuario['code'] != 200:
                return {"message": id_usuario['message']}, id_usuario['code']
            
            user = session.query(Usuario).filter(Usuario.id == id_usuario['message']).first()

            if user:
                data = request.get_json()
                if data.get('nome'):
                    user.nome = data['nome']
                if data.get('telefone'):
                    user.telefone = data['telefone']
                if data.get('cep'):
                    user.cep = data['cep']
                    try:
                        cep_limpo = user.cep.replace("-", "").replace(".", "").strip()
                        if len(cep_limpo) == 8 and cep_limpo.isdigit():
                            res = requests.get(f'https://viacep.com.br/ws/{cep_limpo}/json/', timeout=10)
                            if res.status_code == 200:
                                cep_data = res.json()
                                if not cep_data.get('erro'):
                                    user.logradouro = f"{cep_data.get('logradouro', '')}, {cep_data.get('bairro', '')}"
                                    user.cidade = cep_data.get('localidade', '')
                                    user.estado = cep_data.get('uf', '')
                                    user.pais = 'Brasil'
                    except:
                        pass

                session.commit()
                return {'message': 'Dados atualizados com sucesso'}, 200
            else:
                return {"message": "Usuário não encontrado"}, 404
        finally:
            session.close()