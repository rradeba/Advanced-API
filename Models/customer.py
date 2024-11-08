from extensions import db

class Customer(db.Model):
    __tablename__ = 'customer'

    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False, unique=True)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_role = db.Column(db.String(100), nullable=False)



    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'customer_role' : self.customer_role
        }
    

    