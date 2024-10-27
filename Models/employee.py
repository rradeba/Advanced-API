from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = 'employee'
    employee_id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(100), nullable=False)
    employee_position = db.Column(db.String(100), nullable=False)



    def to_dict(self):
        return {
            'employee_id': self.customer_id,
            'employee_name': self.customer_name,
            'employee_position': self.customer_email,
        }
    
    