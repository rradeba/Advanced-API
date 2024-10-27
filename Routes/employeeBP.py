from flask import Blueprint, jsonify
from flask_limiter import Limiter
from utils.util import get_remote_address
from Controllers.employeeController import save_employee as bp_save_employee, get_employee as bp_get_employee
from decorator import role_required 
from flask_jwt_extended import jwt_required



employee_blueprint = Blueprint('employee', __name__)
limiter = Limiter(key_func=get_remote_address)

@employee_blueprint.route('/', methods=['POST'])
@limiter.limit("5 per minute")
def copy_employee():
    return bp_save_employee()

@employee_blueprint.route('/<int:employee_id>', methods=['GET'])
@limiter.limit("10 per minute")
def pull_employee(employee_id):
    return bp_get_employee(employee_id)



