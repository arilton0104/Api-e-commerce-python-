from flask import Blueprint, request, jsonify
from ..services.payment_service import PaymentService
from ..auth.middleware import token_required

payment_blueprint = Blueprint('payment', __name__)
payment_service = PaymentService()

@payment_blueprint.route('/api/payment/process', methods=['POST'])
@token_required
def process_payment():
    try:
        amount = request.json.get('amount')
        token = request.json.get('token')
        order_id = request.json.get('order_id')

        if not all([amount, token, order_id]):
            return jsonify({'error': 'Dados incompletos'}), 400

        success, result = payment_service.process_payment(amount, token, order_id)

        if success:
            return jsonify({
                'status': 'success',
                'payment_id': result
            })
        else:
            return jsonify({
                'status': 'error',
                'message': result
            }), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payment_blueprint.route('/api/payment/refund/<payment_id>', methods=['POST'])
@token_required
def refund_payment(payment_id):
    try:
        success, result = payment_service.refund_payment(payment_id)

        if success:
            return jsonify({
                'status': 'success',
                'refund_id': result
            })
        else:
            return jsonify({
                'status': 'error',
                'message': result
            }), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500
