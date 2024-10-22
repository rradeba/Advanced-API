from flask import Blueprint, jsonify
from flask_limiter import Limiter
from utils.util import get_remote_address
from Controllers.productionController import save_production, get_production 
from decorator import role_required 



production_blueprint = Blueprint('production', __name__)
limiter = Limiter(key_func=get_remote_address)

@production_blueprint.route('/production', methods=['POST'])
@limiter.limit("5 per minute")
@role_required(required_roles=['admin', 'user']) 
def create_production():
    return save_production()

@production_blueprint.route('/production/<int:production_id>', methods=['GET'])
@limiter.limit("10 per minute")
@role_required(required_roles=['admin', 'user']) 
def fetch_production(production_id):
    return get_production(production_id)
