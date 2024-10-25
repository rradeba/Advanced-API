from flask import Blueprint, jsonify
from flask_limiter import Limiter
from utils.util import get_remote_address
from Controllers.customerController import save_customer as controller_save_customer, get_customer as controller_get_customer
from decorator import role_required 

customer_blueprint = Blueprint('customer', __name__)
limiter = Limiter(key_func=get_remote_address)

@customer_blueprint.route('/customer', methods=['POST'])
@limiter.limit("5 per minute")
 
def create_customer():
    return controller_save_customer()

@customer_blueprint.route('/customer/<int:customer_id>', methods=['GET'])
@limiter.limit("10 per minute")

def get_customer(customer_id):
    return controller_get_customer(customer_id)  
