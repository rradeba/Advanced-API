
from flask import Blueprint, jsonify
from flask_limiter import Limiter
from utils.util import get_remote_address
from Controllers.customerController import save_customer, get_customer, update_customer, delete_customer
from decorator import role_required 
from flask_jwt_extended import jwt_required
from caching import cache 


customer_blueprint = Blueprint('customer', __name__)
limiter = Limiter(key_func=get_remote_address)

@customer_blueprint.route('/', methods=['POST'])
@limiter.limit("5 per minute")
def save_customer_route():
    return save_customer()

@customer_blueprint.route('/get/<int:customer_id>', methods=['GET'])
@limiter.limit("10 per minute")
@cache.cached()
def pull_customer(customer_id):
    return get_customer(customer_id)

@customer_blueprint.route('/put/<int:customer_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
@limiter.limit("10 per minute")
@cache.cached()
def revise_customer(customer_id):
    return update_customer(customer_id)

@customer_blueprint.route('/delete/<int:customer_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
@limiter.limit("10 per minute")
@cache.cached()
def trash_customer(customer_id):
    return delete_customer(customer_id)