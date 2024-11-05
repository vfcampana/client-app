from flask import Flask, request, jsonify, render_template, redirect
from app_configs import Config #Classe de configurações padrões do app
from database import engine
from models.company_user import CompanyUser #Usuario
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from datetime import datetime

app = Flask(__name__)

app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)

# view login
login_manager.login_view = 'login'  # nome da rota

Session = sessionmaker(bind=engine)
session = Session()


@login_manager.user_loader
def load_user(id_empresa):
    return session.query(CompanyUser).get(id_empresa)


app.secret_key = ''

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Autentica o usuário no sistema.

    :return: Mensagens de sucesso ou erro.
    """
    if request.method == "POST":
        data = request.form
        email = data.get("email")
        senha = data.get("senha")

        if email and senha:
            #Pega o primeiro usuario que achar com esse email, logo, só deve poder cadastrar o email 1 vez
            user = session.query(CompanyUser).filter(CompanyUser.email == email).first()
            
            # bcrypt.checkpw(str.encode(senha), str.encode(user.senha)):
            if user and user.senha == senha:
                login_user(user)
                print(current_user.is_authenticated) #Depois de logar o usuario o acesso dele passa a ser por "current_user"
                return jsonify({"message": f"Autenticação bem sucedida {email} : {user.senha}"})

        return jsonify({"message": "Credenciais inválidas"}), 400
    else:
        return render_template("login.html")

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"})


@app.route("/signup", methods=["GET", "POST"])
# A página para criar usuários é apenas para adminstradores do sistema. Para fins de teste, a linha abaixo fica comentada
# para não depender de ter algum admin cadastrado (quando limpa o banco, etc)
#@login_required
def create_user():
    """
    Rota para criação de usuários, sendo mandatório os campos de cnpj, email e senha.

    :return: Mensagem indicando se a criação foi bem sucedida ou não
    """
    if request.method == "POST":
        # depois transformar isso em form data pra usar validadores
        data = request.form
        razao_social = data.get("razao_social")
        cnpj = data.get("cnpj")
        email = data.get("email")
        senha = data.get("senha")
        # valores separados por vírgula, por enquanto
        telefones = data.get("telefones")
        registrado = data.get("registrado")
        atualizado = data.get("atualizado")
        is_admin = data.get("is_admin")

        if cnpj and email and senha:
            #Procura se existe um usuario com esse email
            
            
            db_user = session.query(CompanyUser).filter(CompanyUser.email == email).first()

            #Se nao existir, passa para a fase de criação
            if not db_user: 
                # hashed_password = bcrypt.hashpw(str.encode(senha), bcrypt.gensalt())
                user = CompanyUser(
                    razao_social=razao_social,
                    cnpj=cnpj,
                    email=email,
                    senha=senha,
                    telefones=telefones,
                    registrado=datetime.now(),
                    atualizado=datetime.now(),
                    role='admin' if is_admin else 'user'
                )
                session.add(user)
                session.commit()
            
                return jsonify({"message": "Usuário cadastrado com sucesso"})
            else:
                return jsonify({"message": "Usuário já cadastrado"}), 409
        else:
            return jsonify({"message": "Dados inválidos"}), 401
    else:
        return render_template("index.html")


@app.route('/profile/user/', methods=["GET"])
@login_required
def read_user():
    """
    Rota para visualizar o perfil do usuário logado. Deve mostrar informações do próprio, bem como seus blocos e
    outros.

    :return: Dicionário com informações ou mensagem de erro.
    """

    # need to update the get, it's legacy code now
    user = session.query(CompanyUser).get(current_user.id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"message": "Usuário não identificado"}), 404


@app.route('/user/edit_info', methods=["PUT"])
@login_required
def update_user():
    """
    Rota para alteração de dados do usuário
    
    :return: Mensagem indicando se a criação foi bem sucedida ou não
    """""

    data = request.form
    user = session.query(CompanyUser).get(current_user.id)

    if user and data.get("senha"):
        user.senha = data.get("senha")
        session.commit()
        return jsonify({"message": f"Usuário {current_user.id} atualizado com sucesso."})

    return jsonify({"message": "Usuário não encontrado"}), 404

@app.route('/user/<int:id_user>', methods=["DELETE"])
@login_required
def delete_user(id_user):
    """
    Utilizado apenas por administradores. Caso um cliente deseje não participar mais do sistema, retiramos do banco de
    dados.*

    * Há discussões do que realmente fazer com o registro. Nessa primeira versão, tiramos o registro, mas podemos apenas
    desativar o usuário

    :param id_user: Identificador do usuário a ser deletado.
    :return: Mensagem de sucesso ou erro.
    """
    user = session.query(CompanyUser).get(id_user)

    if id_user == current_user.id or current_user.role != 'admin':
        return jsonify({"message": "Deleção não permitida."}), 403
    else:
        if user:
            session.delete(user)
            session.commit()
            return jsonify({"message": f"Usuário {id_user} deletado com sucesso."})

    return jsonify({"message": "Usuário não encontrado"}), 404


@app.route("/", methods=["GET"])
def initial_page():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)