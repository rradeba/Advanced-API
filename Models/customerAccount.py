
from extensions import db

class CustomerAccount(db.Model):
    __tablename__ = 'customerAccount'

    customer_id = db.Column(db.String, primary_key=True)
    customer_username = db.Column(db.String(100), nullable=False)
    customer_password = db.Column(db.String(100), nullable=False)
    customer_role = db.Column(db.String(100), nullable=False)
    


    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'customer_username': self.customer_username,
            'customer_password': self.customer_password,
            'customer_role': self.customer_role
        }
    

    