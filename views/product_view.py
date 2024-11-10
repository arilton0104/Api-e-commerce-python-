from flask import jsonify
from models.product import Product
from utils.db import db

def add_product_view(data):
    if 'name' in data and 'price' in data:
        product = Product(name=data.get("name"), price=data.get("price"), description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Produto cadastrado com sucesso"}), 201
    else:
        return jsonify({"message": "Dados de produto inválidos"}), 400

def delete_product_view(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": f"Produto com ID {product_id} deletado com sucesso"}), 200
    else:
        return jsonify({"error": "Produto não encontrado"}), 404
    
def update_product_view(product_id, data):
    product = Product.query.get(product_id)
    if product:
        # Update product fields based on provided data
        if 'name' in data:
            product.name = data['name']
        if 'price' in data:
            product.price = data['price']
        if 'description' in data:
            product.description = data.get("description", "")

        # Commit the changes to the database
        db.session.commit()
        return jsonify({"message": f"Produto com ID {product_id} atualizado com sucesso."}), 200
    else:
        return jsonify({"error": "Produto não encontrado."}), 404    

def get_products_view():
    products = Product.query.all()
    products_list = [{'id': product.id, 'name': product.name, 'price': product.price, 'description': product.description} for product in products]
    return jsonify(products_list), 200
