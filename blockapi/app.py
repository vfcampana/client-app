from flask import Flask, request, jsonify, render_template, redirect
from models.extensions import engine
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from datetime import datetime
import bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login' 

app.secret_key = '1234'

Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    app.run(debug=True)