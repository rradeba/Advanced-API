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
    


    