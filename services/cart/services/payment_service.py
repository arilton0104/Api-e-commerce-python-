import stripe
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class PaymentService:
    def __init__(self):
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

    def process_payment(self, amount, token, order_id):
        try:
            payment = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Stripe usa centavos
                currency='brl',
                payment_method=token,
                metadata={'order_id': order_id},
                confirm=True
            )
            
            logger.info(f"Pagamento processado: {payment.id}")
            return True, payment.id
            
        except stripe.error.CardError as e:
            logger.error(f"Erro no cartão: {str(e)}")
            return False, "Erro no cartão"
            
        except Exception as e:
            logger.error(f"Erro no pagamento: {str(e)}")
            return False, str(e)

    def refund_payment(self, payment_id):
        try:
            refund = stripe.Refund.create(payment_intent=payment_id)
            logger.info(f"Reembolso processado: {refund.id}")
            return True, refund.id
        except Exception as e:
            logger.error(f"Erro no reembolso: {str(e)}")
            return False, str(e)
