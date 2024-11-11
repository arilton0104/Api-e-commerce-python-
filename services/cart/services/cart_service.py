import json
import logging
from ..utils.redis_client import redis_client

logger = logging.getLogger(__name__)

class CartService:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def add_item(self, user_id, product_id, quantity):
        try:
            cart = json.loads(self.redis_client.get(f"cart:{user_id}") or "{}")
            
            if str(product_id) in cart:
                cart[str(product_id)]['quantity'] += quantity
            else:
                cart[str(product_id)] = {
                    'product_id': product_id,
                    'quantity': quantity
                }
            
            self.redis_client.set(f"cart:{user_id}", json.dumps(cart))
            logger.info(f"Produto {product_id} adicionado ao carrinho do usuário {user_id}")
            return cart
        except Exception as e:
            logger.error(f"Erro ao adicionar produto: {str(e)}")
            raise

    def remove_item(self, user_id, item_id):
        try:
            cart = json.loads(self.redis_client.get(f"cart:{user_id}") or "{}")
            
            if str(item_id) in cart:
                del cart[str(item_id)]
                self.redis_client.set(f"cart:{user_id}", json.dumps(cart))
                logger.info(f"Item {item_id} removido do carrinho do usuário {user_id}")
            
            return cart
        except Exception as e:
            logger.error(f"Erro ao remover item: {str(e)}")
            raise

    def get_cart(self, user_id):
        try:
            return json.loads(self.redis_client.get(f"cart:{user_id}") or "{}")
        except Exception as e:
            logger.error(f"Erro ao visualizar carrinho: {str(e)}")
            raise

    def clear_cart(self, user_id):
        try:
            self.redis_client.delete(f"cart:{user_id}")
            logger.info(f"Carrinho do usuário {user_id} limpo")
        except Exception as e:
            logger.error(f"Erro ao limpar carrinho: {str(e)}")
            raise

    def calculate_total(self, cart):
        total = 0
        for item in cart.values():
            total += item['price'] * item['quantity']
        return total

    def checkout(self, user_id, payment_data):
        # Lógica de checkout
        pass