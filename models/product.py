from flask_sqlalchemy import SQLAlchemy
from utils.db import db

# Modelo de Produto
# Aqui defini o modelo do produto que será inserido no banco de dados 
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
