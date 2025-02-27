from flask import jsonify
from flask_restful import Resource

class AnuncioList(Resource):
    def get(self):
        return jsonify({'anuncio': 'anuncio'})

class AnuncioGet(Resource):
    def get(self):
        return jsonify({'anuncio': 'anuncio'})

class AnuncioAtualiza(Resource):
    def put(self):
        return jsonify({'anuncio': 'anuncio'})

class AnuncioCadastro(Resource):
    def post(self):
        return jsonify({'anuncio': 'anuncio'})
