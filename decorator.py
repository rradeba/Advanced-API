from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required() 
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            user_roles = current_user.get('roles', '')

            if required_role not in user_roles:
                return jsonify({"message": "Permission denied"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
