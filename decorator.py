from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from Models import user

def role_required(required_roles):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorated(*args, **kwargs):
            current_user_id = get_jwt_identity()  
            user = user.query.get(current_user_id)  
            
            if user is None or user.role not in required_roles:
                return jsonify({'message': 'Access denied. You do not have the required permissions.'}), 403
            
            return fn(*args, **kwargs)
        return decorated
    return wrapper
