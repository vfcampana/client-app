from flask import jsonify, session
from models.ornamental_block import OrnamentalBlock
from database import engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

def filtra_menor_preco():
    """
    Rota para visualizar os blocos do usuário logado.

    :return: Dicionário com informações ou mensagem de erro
    """
    blocos = session.query(OrnamentalBlock).order_by(OrnamentalBlock.valor.asc()).all()
    print(blocos)
    if blocos:
        return [bloco.to_dict() for bloco in blocos]
    return jsonify({"message": "Blocos não identificados"}), 404

def filtra_maior_preco():
    """
    Rota para visualizar os blocos do usuário logado.

    :return: Dicionário com informações ou mensagem de erro
    """
    blocos = session.query(OrnamentalBlock).order_by(OrnamentalBlock.valor.desc()).all()
    if blocos:
        return [bloco.to_dict() for bloco in blocos]
    return jsonify({"message": "Blocos não identificados"}), 404

def filtra_classificacao(classificacao):
    """
    Rota para visualizar os blocos do usuário logado.

    :return: Dicionário com informações ou mensagem de erro
    """
    blocos = session.query(OrnamentalBlock).order_by(OrnamentalBlock.classificao == classificacao).all()
    if blocos:
        return [bloco.to_dict() for bloco in blocos]
    return jsonify({"message": "Blocos não identificados"}), 404

