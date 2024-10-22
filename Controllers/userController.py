from flask import jsonify, request
from Models.user import User 
from extensions import db

def save_user():
   
    data = request.get_json()
    new_user = User(
        user_id=data['user_id'],
        user_username=data['user_name'],
        user_password=data['user_password']
        user_role=data['user_role']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User saved"}), 201

def get_user():
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    users = User.query.paginate(page=page, per_page=per_page, error_out=False)

   
    response = {
        'products': [
            {
                'user_id': user.user_id, 
                'user_username': user.user_username,  
                'user_password': user.user_password,
                'user_role': user.user_role
            } for user in users.items
        ],
        'total': users.total,          
        'pages': users.pages,         
        'current_page': users.page     
    }
    
    
    return jsonify(response), 200