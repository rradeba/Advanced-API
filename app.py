from flask import Flask
from extensions import db, ma, limiter
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from config import config 
from flask_jwt_extended import JWTManager


from Models.customer import Customer
from Models.user import User

from Routes.orderBP import order_blueprint
from Routes.customerBP import customer_blueprint
from Routes.productBP import product_blueprint
from Routes.productionBP import production_blueprint
from Routes.employeeBP import employee_blueprint
from Routes.userBP import user_blueprint

def create_app(config_name):
    app = Flask(__name__)
    if config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    elif config_name == 'development':
        app.config.from_object('config.DevelopmentConfig')
    
 
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    CORS(app)

   
    app.register_blueprint(order_blueprint, url_prefix='/order')
    app.register_blueprint(customer_blueprint, url_prefix='/customer')
    app.register_blueprint(employee_blueprint, url_prefix='/employee')
    app.register_blueprint(product_blueprint, url_prefix='/product')
    app.register_blueprint(production_blueprint, url_prefix='/production')
    app.register_blueprint(user_blueprint, url_prefix='/user')

    return app

def init_customers_info_data(app):
    with app.app_context():
        try:
            customers = [
                Customer(customer_name="Customer One", customer_email="customer1@email.com", customer_phone="1234567890"),
                Customer(customer_name="Customer Two", customer_email="customer2@email.com", customer_phone="1122334455"),
            ]

            customerAccounts = [
                User(user_username="ex1", user_password=generate_password_hash("password1")),
                User(user_username="ex2", user_password=generate_password_hash("password2")),
                User(user_username="ex3", user_password=generate_password_hash("password3")),
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
