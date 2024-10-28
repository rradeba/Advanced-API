from flask import Blueprint, jsonify
from flask_limiter import Limiter
from utils.util import get_remote_address
from Controllers.customerController import save_customer, get_customer 
from decorator import role_required 

customer_blueprint = Blueprint('customer', __name__)
limiter = Limiter(key_func=get_remote_address)

customer_blueprint.route('/', methods=['POST'])(save_customer)
@limiter.limit("5 per minute") 

@customer_blueprint.route('/<int:customer_id>', methods=['GET'])
@limiter.limit("10 per minute")

def pull_customer(customer_id):
    return get_customer(customer_id)  
