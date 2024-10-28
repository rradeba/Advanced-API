from extensions import db



class Production(db.Model):
    __tablename__ = 'production'
    production_id = db.Column(db.Integer, primary_key=True)
    production_quantity = db.Column(db.Integer, nullable=False)
   




    def to_dict(self):
        return {
            'production_id': self.production_id,
            'production_quantity': self.production_quantity
        }
    