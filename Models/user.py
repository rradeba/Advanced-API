from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()



class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.String(100), unique=True, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    user_role = db.Column(db.String(100), nullable=False)

     
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
 