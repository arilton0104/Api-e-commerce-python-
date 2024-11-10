from flask import Flask, request, jsonify
from redis import Redis
import json
from flask_login import login_required
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object('services.cart.config.Config')

# Conexão com Redis
redis_client = Redis(
    host=app.config['REDIS_HOST'],
    port=app.config['REDIS_PORT']
)

@app.route('/api/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    try:
        user_id = str(request.user_id)  # Você precisará implementar autenticação
        quantity = request.json.get('quantity', 1)
        
        cart = json.loads(redis_client.get(f"cart:{user_id}") or "{}")
        
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += quantity
        else:
            cart[str(product_id)] = {
                'product_id': product_id,
                'quantity': quantity
            }
        
        redis_client.set(f"cart:{user_id}", json.dumps(cart))
        logger.info(f"Produto {product_id} adicionado ao carrinho do usuário {user_id}")
        
        return jsonify({"status": "success", "cart": cart})
    except Exception as e:
        logger.error(f"Erro ao adicionar produto: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/cart/remove/<int:item_id>', methods=['DELETE'])
@login_required
def remove_from_cart(item_id):
    try:
        user_id = str(request.user_id)
        cart = json.loads(redis_client.get(f"cart:{user_id}") or "{}")
        
        if str(item_id) in cart:
            del cart[str(item_id)]
            redis_client.set(f"cart:{user_id}", json.dumps(cart))
            logger.info(f"Item {item_id} removido do carrinho do usuário {user_id}")
            
        return jsonify({"status": "success", "cart": cart})
    except Exception as e:
        logger.error(f"Erro ao remover item: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/cart', methods=['GET'])
@login_required
def view_cart():
    try:
        user_id = str(request.user_id)
        cart = json.loads(redis_client.get(f"cart:{user_id}") or "{}")
        return jsonify({"cart": cart})
    except Exception as e:
        logger.error(f"Erro ao visualizar carrinho: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/cart/checkout', methods=['POST'])
@login_required
def checkout():
    try:
        user_id = str(request.user_id)
        cart = json.loads(redis_client.get(f"cart:{user_id}") or "{}")
        
        if not cart:
            return jsonify({"error": "Carrinho vazio"}), 400
            
        # Processar pagamento aqui
        # Criar pedido
        # Atualizar estoque
        
        redis_client.delete(f"cart:{user_id}")
        logger.info(f"Checkout realizado com sucesso para usuário {user_id}")
        
        return jsonify({
            "status": "success",
            "message": "Pedido realizado com sucesso",
            "order": cart
        })
    except Exception as e:
        logger.error(f"Erro no checkout: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
