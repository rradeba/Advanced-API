from flask import Blueprint, jsonify
from flask_limiter import Limiter
from utils.util import get_remote_address
from Controllers.orderController import save_order, get_order
from decorator import role_required 
from flask_jwt_extended import jwt_required
from caching import cache 



order_blueprint = Blueprint('order', __name__)
limiter = Limiter(key_func= get_remote_address)

order_blueprint.route('/', methods=['POST'])
@jwt_required()
@limiter.limit("5 per minute")
@cache.cached()
def save_order_route(order_id):
    return save_order(order_id)

@order_blueprint.route('/<int:order_id>', methods=['GET'])
@jwt_required()
@limiter.limit("10 per minute")
@cache.cached()
def pull_order(order_id):
    return get_order(order_id)



