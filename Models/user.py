from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


from extensions import db

class User(db.Model):
    __tablename__ = 'users'  

    user_id = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.String(100), nullable=False, unique=True)
    user_password = db.Column(db.String(200), nullable=False)
    user_role = db.Column(db.String(50))  

     
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_username': self.user_username,
            'user_role': self.user_role
            
        }
 