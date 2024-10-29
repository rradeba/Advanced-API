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
        customer_phone=data['customer_phone'],
        customer_role=data['customer_role']
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
        'customer_phone': customer.customer_phone,
        'customer_role': customer.customer_role
    }), 200

def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return jsonify({"message": "Customer not found"}), 404

    data = request.get_json()
    if not data or not any(k in data for k in ('customer_name', 'customer_email', 'customer_phone')):
        return jsonify({"message": "Invalid input"}), 400

    if 'customer_name' in data:
        customer.customer_name = data['customer_name']
    if 'customer_email' in data:
        customer.customer_email = data['customer_email']
    if 'customer_phone' in data:
        customer.customer_phone = data['customer_phone']
    if 'customer_role' in data:
        customer.customer_role = data['customer_role']

    db.session.commit()
    return jsonify({"message": "Customer updated"}), 200

def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return jsonify({"message": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted"}), 200



