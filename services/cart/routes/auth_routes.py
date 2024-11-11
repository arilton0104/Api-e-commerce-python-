from flask import Blueprint, request, jsonify
from ..auth.jwt_handler import JWTHandler

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/api/auth/token', methods=['POST'])
def get_token():
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id é obrigatório'}), 400
        
    access_token = JWTHandler.generate_token(user_id)
    refresh_token = JWTHandler.generate_refresh_token(user_id)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
    })

@auth_blueprint.route('/api/auth/refresh', methods=['POST'])
def refresh_token():
    refresh_token = request.json.get('refresh_token')
    if not refresh_token:
        return jsonify({'error': 'refresh_token é obrigatório'}), 400
        
    try:
        data = jwt.decode(refresh_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        new_token = JWTHandler.generate_token(data['user_id'])
        
        return jsonify({'access_token': new_token})
    except:
        return jsonify({'error': 'refresh_token inválido'}), 401
