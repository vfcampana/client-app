from dotenv import load_dotenv
from flask import request, jsonify, current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import jwt

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para retornar o ID e verificar a Validade do Token JWT
def verificar_jwt():
    auth_header = request.headers.get('Authorization')
    resposta = {
        "code": "",
        "message": ""
    }

    if not auth_header:
        resposta['message'] = "Token de autorização não fornecido"
        resposta['code'] = 401
        return resposta

    try:
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            resposta['message'] = "Formato do header Authorization inválido"
            resposta['code'] = 401
            return resposta

        token = parts[1]
        try:
            decoded_token = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=["HS256"]
            )
            resposta['message'] = decoded_token.get('sub')
            resposta['code'] = 200
            return resposta

        except jwt.ExpiredSignatureError:
            resposta['message'] = "Token expirado"
            resposta['code'] = 401
            return resposta

        except jwt.InvalidTokenError as e:
            print(f"Erro JWT: {e}")
            resposta['message'] = "Token inválido"
            resposta['code'] = 401
            return resposta

    except Exception as e:
        resposta['message'] = f"Erro ao processar o token: {str(e)}"
        resposta['code'] = 401
        return resposta
    