import stripe
from flask import jsonify

stripe.api_key = 'sua-chave-stripe'

class PaymentService:
    @staticmethod
    def process_payment(cart_total, token):
        try:
            charge = stripe.Charge.create(
                amount=int(cart_total * 100),
                currency='brl',
                source=token,
                description='Compra E-commerce'
            )
            return True, charge.id
        except stripe.error.StripeError as e:
            return False, str(e)
