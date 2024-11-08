from extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class CustomerAccount(db.Model):
    __tablename__ = 'customerAccount'

    id = db.Column(db.Integer, primary_key=True)  
    customer_id = db.Column(db.Integer, ForeignKey("Customer.customer_id"))
    customer_username = db.Column(db.String(100), unique=True, nullable=False)
    customer_password = db.Column(db.String(128), nullable=False)
    customer_role = db.Column(db.String(100), nullable=False)

    customer = relationship("Customer", back_populates="accounts")

    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'customer_username': self.customer_username,
            'customer_role': self.customer_role
        }


    
    