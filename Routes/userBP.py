from flask import Blueprint, jsonify, request
from flask_limiter import Limiter
from Models.user import User 
from utils.util import get_remote_address
from Controllers.productionController import save_production, get_production 
from decorator import role_required 
from utils.util import encode_token 




user_blueprint = Blueprint('user', __name__)
limiter = Limiter(key_func=get_remote_address)

@user_blueprint.route('/user', methods=['POST'])
@limiter.limit("5 per minute")
@role_required(required_roles=['admin', 'user']) 
def create_production():
    return save_production()

@user_blueprint.route('/user/<int:user_id>', methods=['GET'])
@limiter.limit("10 per minute")
@role_required(required_roles=['admin', 'user']) 
def fetch_production(production_id):
    return get_production(production_id)



@user_blueprint.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = user.query.filter_by(username=username).first()
    
    if user and user.verify_password(password):
        token = encode_token(user.id)
        return jsonify({
            'message': 'Login successful',
            'token': token
        }), 200
    
    return jsonify({'message': 'Bad username or password'}), 401
