from flask import Flask
from models.extensions import engine
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
from api.views import api_bp


app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'supersecretkey' 
jwt = JWTManager(app)

Session = sessionmaker(bind=engine)
session = Session()

app.register_blueprint(api_bp)

socketio = SocketIO(app, cors_allowed_origins='*')

if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True)