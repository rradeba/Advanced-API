from flask import Blueprint, jsonify
from flask_limiter import Limiter
from utils.util import get_remote_address
from Controllers.productController import save_product, get_product
from decorator import role_required 



product_blueprint = Blueprint('product', __name__)
limiter = Limiter(key_func=get_remote_address)

product_blueprint.route('/', methods=['POST'])(save_product)
@limiter.limit("5 per minute")


@product_blueprint.route('/<int:product_id>', methods=['GET'])
@limiter.limit("10 per minute")

def pull_product(product_id):
    return get_product(product_id)
