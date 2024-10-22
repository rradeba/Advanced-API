from flask import jsonify, request
from Models.customer import Customer
from extensions import db

def save_customer():
    data = request.get_json()
    new_customer = Customer(
        customer_id=data['customer_id'], 
        customer_name=data['customer_name'],
        customer_email=data['customer_email'],
        customer_phone=data['customer_phone']
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "Customer saved"}), 201

def get_customer():
   
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

   
    customers = Customer.query.paginate(page=page, per_page=per_page, error_out=False)

    
    response = { 
        'customers': [
            {
                'customer_id': customer.customer_id, 
                'customer_name': customer.customer_name,  
                'customer_email': customer.customer_email,  
                'customer_phone': customer.customer_phone   
            } for customer in customers.items 
        ],
        'total': customers.total,        
        'pages': customers.pages,         
        'current_page': customers.page   
    }
    
    
    return jsonify(response), 200
