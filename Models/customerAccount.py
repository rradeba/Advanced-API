from extensions import db



class CustomerAccount(db.Model):
    __tablename__ = 'CustomerAccount'
    id = db.Column(db.Integer, primary_key=True)  
    customer_username = db.Column(db.String(255), unique=True, nullable=False)
    customer_password = db.Column(db.String(255), nullable=False)
    customer_role = db.Column(db.String(255), nullable=False)

 

    def to_dict(self):
        return {
          
            'customer_username': self.customer_username,
            'customer_password': self.customer_password,
            'customer_role': self.customer_role
        }


    
    