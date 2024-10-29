from flask import Blueprint, jsonify
from flask_limiter import Limiter
from utils.util import get_remote_address
from Controllers.productController import save_product, get_product, update_product, delete_product
from decorator import role_required 
from flask_jwt_extended import jwt_required
from caching import cache 



product_blueprint = Blueprint('product', __name__)
limiter = Limiter(key_func=get_remote_address)

product_blueprint.route('/', methods=['POST'])
@jwt_required()
@role_required 
@limiter.limit("5 per minute")
@cache.cached()
def post_product(product_id):
    return save_product(product_id)


@product_blueprint.route('/get/<int:product_id>', methods=['GET'])
@jwt_required()
@role_required 
@limiter.limit("10 per minute")
@cache.cached()
def pull_product(product_id):
    return get_product(product_id)

@product_blueprint.route('/put/<int:product_id>', methods=['PUT'])
@jwt_required()
@limiter.limit("10 per minute")
@cache.cached()
def revise_product(product_id):
    return update_product(product_id)

@product_blueprint.route('/delete/<int:product_id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("10 per minute")
@cache.cached()
def trash_product(product_id):
    return delete_product(product_id)
