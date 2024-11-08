from flask import Flask
from extensions import db, ma, limiter
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager
from caching import cache

import os
from config import config
from flask_sqlalchemy import SQLAlchemy

from Models.customer import Customer
from Models.customerAccount import CustomerAccount

from Routes.orderBP import order_blueprint
from Routes.customerBP import customer_blueprint
from Routes.customerAccountBP import customer_account_blueprint
from Routes.productBP import product_blueprint
from Routes.loginBP import login_blueprint



def create_app(config):
    app = Flask(__name__)
    
    if config == 'testing':
        app.config.from_object('config.TestingConfig')
    elif config == 'development':
        app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
   
    jwt = JWTManager(app)
    CORS(app)

    
    app.config['CACHE_TYPE'] = 'simple'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    cache.init_app(app)

    app.register_blueprint(order_blueprint, url_prefix='/order')
    app.register_blueprint(customer_blueprint, url_prefix='/customer')
    app.register_blueprint(customer_account_blueprint, url_prefix='/customer_account')
    app.register_blueprint(product_blueprint, url_prefix='/product')
    app.register_blueprint(login_blueprint, url_prefix='/login')
    return app

def init_customers_info_data(app):
    with app.app_context():
        try:
            Customer.query.delete()
            db.session.commit()
            
            customers = [
                Customer(customer_id=1, customer_name="Customer One", customer_email="customer1@email.com", customer_phone="1234567890", customer_role="admin"),
                Customer(customer_id=2, customer_name="Customer Two", customer_email="customer2@email.com", customer_phone="1122334455", customer_role="admin"),
            ]
            db.session.add_all(customers)
            db.session.commit() 
            

            CustomerAccount.query.delete()
            db.session.commit()

            customer_accounts = [
                CustomerAccount(id=5,customer_username="ex1",customer_password=generate_password_hash("password1"), customer_role="admin"),
                CustomerAccount(id=6, customer_username="ex2",customer_password=generate_password_hash("password2"), customer_role="admin")
            ]

            db.session.add_all(customer_accounts)
            db.session.commit()  
            print("Customer data initialized successfully.")
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing customer data: {e}")
            print([rule.rule for rule in app.url_map.iter_rules()])



if __name__ == '__main__':
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        init_customers_info_data(app)
        app.run(debug=True)
