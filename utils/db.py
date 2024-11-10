from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    # Cria apenas tabelas que ainda não existem
    db.create_all()
