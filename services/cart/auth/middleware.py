from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token ausente'}), 401
            
        try:
            token = token.split(' ')[1]  # Remove 'Bearer '
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            
            if datetime.fromtimestamp(data['exp']) < datetime.utcnow():
                return jsonify({'error': 'Token expirado'}), 401
                
            request.user_id = data['user_id']
            return f(*args, **kwargs)
            
        except Exception as e:
            return jsonify({'error': 'Token inválido'}), 401
            
    return decorated
