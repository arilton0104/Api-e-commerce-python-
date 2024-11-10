from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from utils.db import db

auth_blueprint = Blueprint('auth', __name__)

# Rota de login
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Consulta o usuário no banco de dados
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({"message": "Login realizado com sucesso"})
    else:
        return jsonify({"error": "Usuário ou senha inválidos"}), 401

# Rota de registro
@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Usuário já existe"}), 400
    
    # Cria um novo usuário
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registro realizado com sucesso"}), 201

# Rota de logout
@auth_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso"})

# Rota protegida de exemplo
@auth_blueprint.route('/protected', methods=['GET'])
@login_required
def protected():
    return jsonify({"message": f"Bem-vindo {current_user.username}, você acessou uma rota protegida!"})
