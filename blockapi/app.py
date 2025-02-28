from flask import Flask
from models.extensions import engine
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager
from flask_cors import CORS
from api.views import api_bp
from models.extensions import login_manager

app = Flask(__name__)
CORS(app)

login_manager.init_app(app)

login_manager.login_view = 'login' 

app.secret_key = '1234'

Session = sessionmaker(bind=engine)
session = Session()

app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)