from flask import jsonify
from flask_restful import Resource

class Bloco(Resource):
    def get(self):
        return jsonify({'bloco': 'bloco'})
