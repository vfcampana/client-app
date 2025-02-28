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
        "code" : "",
        "message": ""
    }
    
    if not auth_header:
        resposta['message'] = "Token de autorização não fornecido"
        resposta['code'] = 401
    
    try:
        token = auth_header.split(" ")[1]
        
        try:
            decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"], options={"verify_sub": False})
            resposta['message'] = decoded_token['sub']
            resposta['code'] = 200
        
        except Exception as e:
            resposta['message'] = "Erro ao decodificar o token"
            resposta['code'] = 401
            
    except jwt.ExpiredSignatureError:
        resposta['message'] =  "Token expirado"
        resposta['code'] = 401
    
    except jwt.InvalidTokenError:
        resposta['message'] =  "Token inválido"
        resposta['code'] = 401
        
    except:
        resposta['message'] = "Token ausente"
        resposta['code'] = 401
        
    return resposta