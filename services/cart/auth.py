from functools import wraps
import jwt
from flask import request, jsonify

def create_token(user_id):
    return jwt.encode(
        {'user_id': user_id},
        'seu-segredo',
        algorithm='HS256'
    )

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token ausente'}), 401
        try:
            data = jwt.decode(token, 'seu-segredo', algorithms=['HS256'])
            request.user_id = data['user_id']
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Token inválido'}), 401
    return decorated
