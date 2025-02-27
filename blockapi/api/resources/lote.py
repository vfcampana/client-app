from flask import jsonify
from flask_restful import Resource

class LoteList(Resource):
    def get(self):
        return jsonify({'lote': 'lote'})

class LoteGet(Resource):
    def get(self):
        return jsonify({'lote': 'lote'})

class LoteAtualiza(Resource):
    def put(self):
        return jsonify({'lote': 'lote'})

class LoteCadastro(Resource):
    def post(self):
        return jsonify({'lote': 'lote'})
