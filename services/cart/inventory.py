class InventoryService:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def update_stock(self, product_id, quantity):
        current = int(self.redis_client.get(f"stock:{product_id}") or 0)
        new_quantity = current - quantity
        
        if new_quantity < 0:
            return False, "Estoque insuficiente"
            
        self.redis_client.set(f"stock:{product_id}", new_quantity)
        return True, new_quantity

    def check_stock(self, product_id, quantity):
        current = int(self.redis_client.get(f"stock:{product_id}") or 0)
        return current >= quantity
