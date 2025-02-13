from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db


class User(db.Model, UserMixin):
    __tablename__ = 'users_cocktail'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    cocktails = db.relationship('Cocktail', back_populates='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Cocktail(db.Model):
    __tablename__ = 'cocktails'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    cup = db.Column(db.String, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    ingredients = db.Column(db.JSON, nullable=False)  
    color = db.Column(db.String, nullable=False)
    sweetness = db.Column(db.Float, default=0)
    bitterness = db.Column(db.Float, default=0)
    smoothness = db.Column(db.Float, default=0)
    strength = db.Column(db.Float, default=0)
    freshness = db.Column(db.Float, default=0)
    enjoyment_rating = db.Column(db.Float, default=0)
    final_strength = db.Column(db.Float, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey(''), nullable=False)

    user = db.relationship('User', back_populates='cocktails')

    def __repr__(self):
        return f'<Cocktail {self.name}>'
