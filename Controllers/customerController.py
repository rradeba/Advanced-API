from flask import jsonify, request
from Models.customer import Customer
from extensions import db



def save_customer():
    data = request.get_json()
    if not data or not all(k in data for k in ('customer_id', 'customer_name', 'customer_email', 'customer_phone')):
        return jsonify({"message": "Invalid input"}), 400
    
    new_customer = Customer(
        customer_id=data['customer_id'], 
        customer_name=data['customer_name'],
        customer_email=data['customer_email'],
        customer_phone=data['customer_phone']
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "Customer saved"}), 201
    

def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return jsonify({"message": "Customer not found"}), 404

    return jsonify({
        'customer_id': customer.customer_id,
        'customer_name': customer.customer_name,
        'customer_email': customer.customer_email,
        'customer_phone': customer.customer_phone
    }), 200



