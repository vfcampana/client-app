from flask import jsonify
from flask_restful import Resource

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
        return jsonify({'bloco': 'bloco'})
