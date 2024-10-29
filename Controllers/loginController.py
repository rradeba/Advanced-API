from flask import jsonify, request
from Models.customerAccount import CustomerAccount
from extensions import db

from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

def login():
    customer_username = request.json.get('username')
    customer_password = request.json.get('password')

    if not customer_username or not customer_password:
        return jsonify({"msg": "Username and password required"}), 400

    customer = CustomerAccount.query.filter_by(customer_username=customer_username).first()
    if customer and check_password_hash(customer.customer_password, customer_password):
        access_token = create_access_token(identity={"username": customer_username, "role": customer.customer_role})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401
