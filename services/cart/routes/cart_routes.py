from flask import Blueprint, request, jsonify
from ..controllers.cart_controller import CartController
from ..auth.middleware import token_required

cart_blueprint = Blueprint('cart', __name__)

@cart_blueprint.route('/api/cart/add/<int:product_id>', methods=['POST'])
@token_required
def add_to_cart(product_id):
    return CartController.add_to_cart(request.user_id, product_id, request.json)

@cart_blueprint.route('/api/cart/remove/<int:item_id>', methods=['DELETE'])
@auth_required
def remove_from_cart(item_id):
    return CartController.remove_from_cart(request.user_id, item_id)

@cart_blueprint.route('/api/cart', methods=['GET'])
@auth_required
def view_cart():
    return CartController.view_cart(request.user_id)

@cart_blueprint.route('/api/cart/checkout', methods=['POST'])
@auth_required
def checkout():
    return CartController.checkout(request.user_id, request.json)