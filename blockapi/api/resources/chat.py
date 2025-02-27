from flask import jsonify
from flask_restful import Resource

class ChatList(Resource):
    def get(self):
        return jsonify({'chat': 'chat'})

class ChatGet(Resource):
    def get(self):
        return jsonify({'chat': 'chat'})

class EnviarMensagem(Resource):
    def post(self):
        return jsonify({'mensagem': 'mensagem'})
