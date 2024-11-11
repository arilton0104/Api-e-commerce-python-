from flask import Blueprint, request, jsonify
import stripe

webhook_blueprint = Blueprint('webhook', __name__)

@webhook_blueprint.route('/api/webhook/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, current_app.config['STRIPE_WEBHOOK_SECRET']
        )

        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object
            # Atualizar status do pedido
            order_id = payment_intent.metadata.get('order_id')
            # Implementar lógica de atualização

        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Adicionando o webhook para receber notificações do Stripe: