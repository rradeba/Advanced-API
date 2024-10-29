from flask import Blueprint, jsonify, request 
from flask_limiter import Limiter
from utils.util import get_remote_address
from Controllers.loginController import login
from caching import cache 



login_blueprint = Blueprint('login', __name__)
limiter = Limiter(key_func=get_remote_address)

@login_blueprint.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
@cache.cached()

def pull_order(order_id):
    return login(order_id)



