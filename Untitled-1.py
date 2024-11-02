#Controller File:
from flask import jsonify, request
from Models.product import Product 
from extensions import db

def save_product():
    data = request.get_json()
    if not data or not all(k in data for k in ('product_id', 'product_name', 'product_price')):
        return jsonify({"message": "Invalid input"}), 400
    
    new_product = Product(
        product_id=data['product_id'],
        product_name=data['product_name'],
        product_price=data['product_price']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product saved"}), 201

def get_product(product_id):
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"message": "Product not found"}), 404

    response = {
        'product_id': product.product_id, 
        'product_name': product.product_name,  
        'product_price': product.product_price 
    }
    
    return jsonify(response), 200

def update_product(product_id):
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"message": "Product not found"}), 404

    data = request.get_json()
    if not data or not any(k in data for k in ('product_name', 'product_price')):
        return jsonify({"message": "Invalid input"}), 400

    if 'product_name' in data:
        product.product_name = data['product_name']
    if 'product_price' in data:
        product.product_price = data['product_price']

    db.session.commit()
    return jsonify({"message": "Product updated"}), 200

def delete_product(product_id):
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"message": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200

def list_products():
    products = Product.query.all()
    response = []
    
    for product in products:
        response.append({
            'product_id': product.product_id,
            'product_name': product.product_name,
            'product_price': product.product_price
        })
    
    return jsonify(response), 200

    

#Route File: 

from flask import Blueprint, jsonify
from flask_limiter import Limiter
from utils.util import get_remote_address
from Controllers.productController import save_product, get_product, update_product, delete_product
from decorator import role_required 
from flask_jwt_extended import jwt_required



product_blueprint = Blueprint('product', __name__)
limiter = Limiter(key_func=get_remote_address)

product_blueprint.route('/', methods=['POST'])(save_product)
@jwt_required 
@limiter.limit("5 per minute")


@product_blueprint.route('/<int:product_id>', methods=['GET'])
@jwt_required 
@limiter.limit("10 per minute")

def pull_product(product_id):
    return get_product(product_id)

@product_blueprint.route('/<int:customer_id>', methods=['PUT'])
@jwt_required 
@limiter.limit("10 per minute")

def revise_customer(customer_id):
    return update_product(customer_id)

@product_blueprint.route('/<int:customer_id>', methods=['DELETE'])
@jwt_required 
@limiter.limit("10 per minute")

def trash_customer(customer_id):
    return delete_product(customer_id)

#model 
from extensions import db

class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_price = db.Column(db.Float, nullable=False)




def to_dict(self):
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_price': self.product_price
        }
    


    



#config file: 

class Config:
    SECRET_KEY = 'key'  
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = '3600'
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db' 
    

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/prod_db'  

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  
    

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}


#extensions file 

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


limiter = Limiter(
    key_func= get_remote_address,
    default_limits=["100 per hour"]  
)

db = SQLAlchemy()


ma = Marshmallow()



#decorations file
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required() 
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            user_roles = current_user.get('roles', [])

            if required_role not in user_roles:
                return jsonify({"message": "Permission denied"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator

#app file 

from flask import Flask
from extensions import db, ma, limiter
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from config import config 
from flask_jwt_extended import JWTManager


from Models.customer import Customer
from Models.customerAccount import CustomerAccount 
from Routes.orderBP import order_blueprint
from Routes.customerBP import customer_blueprint
from Routes.customerAccountBP import customer_account_blueprint
from Routes.productBP import product_blueprint
from Routes.loginBP import login_blueprint 


def create_app(config_name):
    app = Flask(__name__)
    if config_name == 'testing':
        config.from_object('config.TestingConfig')
    elif config_name == 'development':
        config.from_object('config.DevelopmentConfig')
    
    jwt = JWTManager(app)
 
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    CORS(app)

   
    app.register_blueprint(order_blueprint, url_prefix='/order')
    app.register_blueprint(customer_blueprint, url_prefix='/customer')
    app.register_blueprint(customer_account_blueprint, url_prefix='/customer_account')
    app.register_blueprint(product_blueprint, url_prefix='/product')
    

    return app

def init_customers_info_data(app):
    with app.app_context():
        try:
            customers = [
                Customer(customer_name="Customer One", customer_email="customer1@email.com", customer_phone="1234567890"),
                Customer(customer_name="Customer Two", customer_email="customer2@email.com", customer_phone="1122334455"),
            ]

            customerAccounts = [
                CustomerAccount(custmer_username="ex1", customer_password=generate_password_hash("password1")),
                CustomerAccount(customer_username="ex2", customer_password=generate_password_hash("password2")),
                CustomerAccount(customer_username="ex3", customer_password=generate_password_hash("password3")),
            ]

            db.session.add_all(customers)
            db.session.add_all(customerAccounts)
            db.session.commit()
            print("Customer data initialized successfully.")
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing customer data: {e}")

if __name__ == '__main__':
    app = create_app('development')  
    
    with app.app_context():
        db.create_all()
        init_customers_info_data(app)
        app.run(debug=True)
