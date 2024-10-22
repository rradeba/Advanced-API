from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class Production(db.Model):
    __tablename__ = 'production'
    production_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    production_quantity = db.Column(db.Integer, nullable=False)
    production_date = db.Column(db.Date, nullable=False)




    def to_dict(self):
        return {
            'production_id': self.production_id,
            'product_id': self.product_id,
            'production_quantity': self.production_quantity,
            'production_date': self.production_date
        }
    