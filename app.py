from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from utils.db import db, init_db
from controllers.auth_controller import auth_blueprint
from controllers.product_controller import product_blueprint
from models.user import User
import colorama
import pymysql

pymysql.install_as_MySQLdb()

# Inicializa o app Flask
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Inicializa extensões
    db.init_app(app)
    CORS(app)
    
    # Configuração do LoginManager
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'  # Redireciona para /login se o usuário não está autenticado
    
    # Função para carregar o usuário pelo ID
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))


    # Registra Blueprints (módulos de rotas)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(product_blueprint)

    # Inicializa o banco de dados
    with app.app_context():
        init_db()

    return app

colorama.init()

# Executa o app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)



# comando pra rodar a aplicação

#   python app.py
