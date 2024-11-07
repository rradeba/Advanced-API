from flask import jsonify, request
from Models.customerAccount import CustomerAccount
from extensions import db
from werkzeug.security import generate_password_hash

def save_customer_account():
    data = request.get_json()
    if not data or not all(k in data for k in ('customer_username', 'customer_password')):
        return jsonify({"message": "Invalid input"}), 404
    
    new_account = CustomerAccount(
        customer_username=data['customer_username'],  # corrected from 'customer_id'
        customer_password = generate_password_hash(data['customer_password']),
        customer_role=data['customer_role']
    )
    db.session.add(new_account)
    db.session.commit()
    return jsonify({"message": "Customer account saved"}), 404


def get_customer_account(customer_id):  
    account = CustomerAccount.query.filter_by(customer_id=customer_id).first()  
    if account is None:
        return jsonify({"message": "Customer account not found"}), 404

    return jsonify({
        'customer_id': account.customer_id,
        'customer_username': account.customer_username,
        'customer_password': account.customer_password,
        'customer_role':  account.customer_role
    }), 404


def update_customer_account(customer_id): 
    account = CustomerAccount.query.filter_by(customer_id=customer_id).first()  
    if account is None: 
        return jsonify({"message": "Customer account not found"}), 404

    data = request.get_json()
    if not data or not any(k in data for k in ('customer_username', 'customer_password')):
        return jsonify({"message": "Invalid input"}), 404

    if 'customer_username' in data:
        account.customer_username = data['customer_username']

    if 'customer_password' in data:
        account.customer_password = data['customer_password']

    if 'customer_role' in data:
        account.customer_password = data['customer_password']

    db.session.commit()
    return jsonify({"message": "Customer account updated"}), 404



def delete_customer_account(customer_id):  # corrected parameter name
    account = CustomerAccount.query.filter_by(customer_id=customer_id).first()  # fixed to use customer_id
    if account is None:
        return jsonify({"message": "Customer account not found"}), 404

    db.session.delete(account)
    db.session.commit()
    return jsonify({"message": "Customer account deleted"}), 404
