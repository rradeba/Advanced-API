from flask import Blueprint, jsonify
from flask_limiter import Limiter
from utils.util import get_remote_address
from Controllers.customerAccountController import (
    save_customer_account,
    get_customer_account,
    update_customer_account,
    delete_customer_account,
)
from decorator import role_required
from flask_jwt_extended import jwt_required
from caching import cache

customer_account_blueprint = Blueprint('customer_account', __name__)
limiter = Limiter(key_func=get_remote_address)

@customer_account_blueprint.route('/', methods=['POST'])
@jwt_required()
@role_required('admin')
@limiter.limit("5 per minute") 
@cache.cached()
def create_customer_account():  
    return save_customer_account() 

@customer_account_blueprint.route('/get/<int:customer_account_id>', methods=['GET'])
@jwt_required()
@role_required('admin')
@limiter.limit("10 per minute")
@cache.cached()
def retrieve_customer_account(customer_account_id): 
    return get_customer_account(customer_account_id)

@customer_account_blueprint.route('/put/<int:customer_account_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
@limiter.limit("10 per minute")
@cache.cached()
def update_customer_account_route(customer_account_id):  
    return update_customer_account(customer_account_id)

@customer_account_blueprint.route('/delete/<int:customer_account_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
@limiter.limit("10 per minute")
@cache.cached()
def delete_customer_account_route(customer_account_id): 
    return delete_customer_account(customer_account_id)
