from flask import jsonify
from models.user import User
from flask_login import login_user, current_user, login_required, logout_user
from utils.db import db
from werkzeug.security import check_password_hash
import logging
import re

def login_view(data):
    try:
        # Validação básica dos dados de entrada
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"message": "Nome de usuário e senha são obrigatórios"}), 400

        # Tenta consultar o banco de dados pelo nome de usuário
        user = User.query.filter_by(username=username).first()

        # Verifica se o usuário existe e a senha está correta
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return jsonify({"message": "Conectado com sucesso"}), 200
        else:
            return jsonify({"message": "Não autorizado. Credenciais inválidas"}), 401

    except Exception as e:
        logging.error(f"Erro ao conectar com o banco de dados: {e}")
        return jsonify({"message": "Erro ao conectar com o banco de dados"}), 500


def register_view(data):
    try:
        username = data.get("username")
        password = data.get("password")

        # Validação do nome de usuário e senha
        if not username or not password:
            return jsonify({"message": "Nome de usuário e senha são obrigatórios"}), 400
        if len(password) < 6:
            return jsonify({"message": "A senha deve ter pelo menos 6 caracteres"}), 400

        # Validação de formato seguro para o nome de usuário
        if not re.match("^[a-zA-Z0-9_.-]+$", username):
            return jsonify({"message": "Nome de usuário inválido"}), 400

        # Verifica se o usuário já existe
        if User.query.filter_by(username=username).first():
            return jsonify({"message": "Nome de usuário já existe"}), 409

        # Cria um novo usuário com senha hash e adiciona ao banco
        new_user = User(username=username)
        new_user.set_password(password)  # Armazena a senha hashada

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Usuário registrado com sucesso"}), 201

    except Exception as e:
        logging.error(f"Erro ao registrar no banco de dados: {e}")
        return jsonify({"message": "Erro ao registrar no banco de dados"}), 500

# Rota para logout
def logout_view():
    logout_user()
    return jsonify({"message": "Desconectado com sucesso"}), 200



#Agora, para adicionar segurança nas rotas e autenticação de usuário, vamos melhorar a arquitetura com algumas funcionalidades adicionais:

#Autenticação:

#Implementaremos segurança com Flask-Login para gerenciar sessões e proteger as rotas.
#Utilizaremos @login_required nas rotas que precisam de autenticação para limitar o acesso apenas a usuários autenticados.
#Proteção das Rotas:

#Somente usuários autenticados poderão acessar determinadas rotas.







#Explicação do Código:
#Login: Verifica se o username e password são válidos e faz login usando login_user.
#Registro: Cria um novo usuário e aplica um hash na senha.
#Logout: Termina a sessão atual do usuário usando logout_user.
#Proteção de Rotas: A rota /protected é protegida com @login_required, e somente usuários autenticados podem acessá-la.
#4. Testando a Segurança
#Registro: Envie uma requisição POST para /register com username e password no corpo para criar um novo usuário.
#Login: Envie uma requisição POST para /login com as credenciais para autenticar o usuário.
#Acesso a Rota Protegida: Envie uma requisição GET para /protected. Se o usuário estiver autenticado, receberá uma mensagem de sucesso; caso contrário, será redirecionado para a rota de login.
#Logout: Envie uma requisição POST para /logout para encerrar a sessão do usuário atual.
#Agora, sua aplicação possui um sistema de segurança básico com proteção de rotas usando autenticação e gerenciamento de sessão com Flask-Login.





#Para aprimorar a segurança na autenticação e cadastro de usuários, podemos implementar algumas melhorias na sua views/auth_view.py:

#Validação e sanitização dos dados de entrada: Isso evita injeção de dados inesperados.
#Taxas de tentativas de login (rate-limiting): Previne tentativas de força bruta.
#Gerenciamento de sessões com cookies seguros: Configurando session_protection, remember me e secure cookies.
#Autenticação de rota protegida por login: Usando o decorador @login_required. 


#Explicação das Modificações
#Validação de Entrada: Valida se o username e password são fornecidos. Também foi incluída uma regra básica para nomes de usuário (^[a-zA-Z0-9_.-]+$) e uma verificação do comprimento da senha.
#Hash de Senha: Garantimos que a senha seja verificada com check_password_hash para não armazenar senhas em texto puro.
#Logout com logout_view: Implementamos um logout seguro com a função logout_user.
#Tratamento de Erros com Logging: Log de erros quando ocorre falha no banco de dados, permitindo um melhor acompanhamento de possíveis problemas.
#Com essas melhorias, sua aplicação fica mais segura e robusta para autenticação e gerenciamento de usuários.

#Não, na arquitetura MVC (Model-View-Controller), a camada de **View** não é a mesma coisa que a camada de **Service**. Cada uma tem funções específicas dentro da estrutura do MVC, que é uma forma de organizar a aplicação para separar as responsabilidades de forma clara:

### 1. **View**
  #- A camada de **View** é responsável por apresentar as informações ao usuário, ou seja, é a camada de interface. No contexto de uma aplicação web, isso inclui as páginas HTML, componentes de interface e, possivelmente, scripts JavaScript que interagem diretamente com o usuário.
   #- A View recebe dados do **Controller** e os exibe, mas não contém a lógica de negócio em si.

### 2. **Service**
  #- A camada de **Service** não é uma parte oficial do MVC, mas é frequentemente usada em conjunto para organizar a lógica de negócio. 
   #- Ela é responsável por implementar as regras de negócio e processos complexos da aplicação. Em aplicações maiores, a lógica de negócio fica na camada de **Service** para que o **Controller** fique mais simples, servindo principalmente como intermediário entre o **Service** e a **View**.
   #- Assim, os Services funcionam como intermediários entre o **Model** (que representa os dados e a lógica de acesso aos dados) e o **Controller**.

### 3. **Controller**
   #- O **Controller** é o ponto central de comunicação entre a View e os Models (e, frequentemente, os Services).
   #- Ele recebe as requisições do usuário pela View, interage com o Model (ou com os Services) para obter ou atualizar dados, e então repassa os dados processados de volta à View para que sejam apresentados.

### Resumindo
#No MVC, a View é a camada de apresentação, enquanto o Service é uma camada adicional que cuida da lógica de negócio.