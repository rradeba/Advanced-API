from flask import Flask
from extensions import db, ma, limiter
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from utils.util import encode_token 

from Models.customer import Customer
from Models.employee import Employee
from Models.product import Product
from Models.production import Production
from Models.order import Order
from Models.user import User 

from Routes.orderBP import order_blueprint
from Routes.customerBP import customer_blueprint
from Routes.productBP import product_blueprint
from Routes.productionBP import production_blueprint
from Routes.employeeBP import employee_blueprint
from Routes.userBP import user_blueprint


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(f'config.{config_name}')
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    CORS(app)

    
    app.register_blueprint(order_blueprint, url_prefix='/orders')
    app.register_blueprint(customer_blueprint, url_prefix='/customers')
    app.register_blueprint(employee_blueprint, url_prefix='/employees')
    app.register_blueprint(product_blueprint, url_prefix='/products')
    app.register_blueprint(production_blueprint, url_prefix='/productions')
    app.register_blueprint(user_blueprint, url_prefix='/user')

    

    return app  # Return the app instance



if __name__ == '__main__':
    app = create_app('DevelopmentConfig') 
    with app.app_context():
        db.create_all() 
        app.run(debug=True)


def configure_rate_limit():
    # Rate limit applied to the customer routes
    limiter.limit("5 per day")(customer_blueprint)




def init_customers_info_data():
    with Session(db.engine) as session:
        with session.begin():
            # Creating customer data
            customers = [
                Customer(customer_name="Customer One", customer_email="customer1@email.com", customer_phone="1234567890"),
                Customer(customer_name="Customer Two", customer_email="customer2@email.com", customer_phone="1122334455"),
            ]

            # Creating customer account data with hashed passwords
            customerAccounts = [
                User(user_username="ex1", user_password=generate_password_hash("password1")),
                User(user_username="ex2", user_password=generate_password_hash("password2")),
                User(user_username="ex3", user_password=generate_password_hash("password3")),
            ]

            session.add_all(customers)
            session.add_all(customerAccounts)
            session.commit()  

configure_rate_limit()
init_customers_info_data()  