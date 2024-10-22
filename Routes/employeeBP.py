from flask import Blueprint, jsonify
from flask_limiter import Limiter
from utils.util import get_remote_address
from Controllers.employeeController import save_employee, get_employee
from decorator import role_required 



employee_blueprint = Blueprint('employee', __name__)
limiter = Limiter(key_func=get_remote_address)

@employee_blueprint.route('/employee', methods=['POST'])
@limiter.limit("5 per minute")
@role_required(required_roles=['admin', 'user']) 
def create_employee():
    return save_employee()

@employee_blueprint.route('/employee/<int:employee_id>', methods=['GET'])
@limiter.limit("10 per minute")
@role_required(required_roles=['admin', 'user']) 
def fetch_employee(employee_id):
    return get_employee(employee_id)



