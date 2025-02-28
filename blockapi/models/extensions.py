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
    
    if not auth_header:
        response = jsonify({"message": "Token de autorização não fornecido"})
        response.status_code = 401
        return response
    
    try:
        token = auth_header.split(" ")[1]
        
        try:
            decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"], options={"verify_sub": False})
            id_usuario = decoded_token['sub']
            return id_usuario
        
        except Exception as e:
            response = jsonify({"message": "Erro ao decodificar o token", "error": str(e)})
            response.status_code = 401
            return response
        
    except jwt.ExpiredSignatureError:
        response = jsonify({"message": "Token expirado"})
        response.status_code = 401
        return response
    
    except jwt.InvalidTokenError:
        response = jsonify({"message": "Token inválido"})
        response.status_code = 401
        return response