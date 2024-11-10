from flask import Blueprint, request
from flask_login import login_required
from views.product_view import add_product_view, delete_product_view, get_products_view, update_product_view

product_blueprint = Blueprint('products', __name__)

# Rota para adicionar produtos (protegida)
@product_blueprint.route('/api/products/add', methods=["POST"])
@login_required
def add_product():
    data = request.json
    return add_product_view(data)

# Rota para deletar um produto pelo ID (protegida)
@product_blueprint.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required
def delete_product(product_id):
    return delete_product_view(product_id)

# Rota para listar todos os produtos
@product_blueprint.route('/api/products', methods=['GET'])
def get_products():
    return get_products_view()

# Rota para atualizar um produto pelo ID (protegida)
@product_blueprint.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required
def update_product(product_id):
    data = request.json
    return update_product_view(product_id, data)
