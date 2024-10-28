from flask import Blueprint, jsonify
from flask_limiter import Limiter
from utils.util import get_remote_address
from Controllers.orderController import save_order, get_order
from decorator import role_required 



order_blueprint = Blueprint('order', __name__)
limiter = Limiter(key_func= get_remote_address)

order_blueprint.route('/', methods=['POST'])(save_order)
@limiter.limit("5 per minute")


@order_blueprint.route('/<int:order_id>', methods=['GET'])
@limiter.limit("10 per minute")

def pull_order(order_id):
    return get_order(order_id)



