from flask import jsonify
from ..services.cart_service import CartService
import logging

logger = logging.getLogger(__name__)

class CartController:
    @staticmethod
    def add_to_cart(user_id, product_id, quantity):
        try:
            cart = CartService.add_item(user_id, product_id, quantity)
            logger.info(f"Produto {product_id} adicionado ao carrinho do usuário {user_id}")
            return jsonify({"status": "success", "cart": cart})
        except Exception as e:
            logger.error(f"Erro ao adicionar produto: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def remove_from_cart(user_id, item_id):
        try:
            cart = CartService.remove_item(user_id, item_id)
            logger.info(f"Item {item_id} removido do carrinho do usuário {user_id}")
            return jsonify({"status": "success", "cart": cart})
        except Exception as e:
            logger.error(f"Erro ao remover item: {str(e)}")
            return jsonify({"error": str(e)}), 500
