from extensions import db

class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True)
    order_quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)




    def to_dict(self):
        return {
            'order_id': self.order_id,
            'order_quantity': self.order_quantity,
            'total_price': self.total_price
        }
    