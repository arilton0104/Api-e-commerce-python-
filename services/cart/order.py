from datetime import datetime

class OrderService:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def create_order(self, user_id, cart, payment_id):
        order = {
            'order_id': self._generate_order_id(),
            'user_id': user_id,
            'items': cart,
            'payment_id': payment_id,
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
        
        self.redis_client.set(
            f"order:{order['order_id']}", 
            str(order)
        )
        return order

    def _generate_order_id(self):
        return datetime.now().strftime('%Y%m%d%H%M%S')
