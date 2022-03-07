from math import prod
import os
from base64 import b64encode
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask import current_app
from api import db
from api.lib.models import ResourceMixin


class Product(db.Model, ResourceMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), index=True, unique=True, nullable=False)
    category = db.Column(db.String(255), index=True, nullable=False)
    sub_category = db.Column(db.String(255), index=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    colors = db.Column(db.Text)
    sizes = db.Column(db.Text)
    images = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    inventory = db.Column(db.Integer, default=0)
    discount = db.Column(db.Float, nullable=False)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'))
    
    def __repr__(self):
        return f'<Product {self.id}>'

    def gen_slug(self, name):
        return f"{name.replace(' ', '-').lower()}-{b64encode(os.urandom(8)).decode('utf-8').rstrip('=')}"


class Merchant(db.Model, ResourceMixin):
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), index=True, unique=True, nullable=False)
    store_location = db.Column(db.String(255))
    store_photo = db.Column(db.String(255))
    store_banner = db.Column(db.String(255))
    fullName = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    phone = db.Column(db.String(14), nullable=False)
    products = db.relationship('Product', backref='merchant', lazy='dynamic')
    
    def __repr__(self):
        return f'<Merchant: {self.store_name}>'
    
    def gen_slug(self, name):
        return f"{name.replace(' ', '-').lower()}-{b64encode(os.urandom(8)).decode('utf-8').rstrip('=')}"


user_wishlist = db.Table('wishlist',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)


class User(db.Model, ResourceMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255), index=True, nullable=False)
    lastName = db.Column(db.String(255), index=True, nullable=False)
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), default='password')
    phone = db.Column(db.String(14), index=True)
    address = db.Column(db.String(255), index=True)
    photo = db.Column(db.String(255))
    wishlist = db.relationship('Product', secondary=user_wishlist, lazy="dynamic", backref='wishers')
    
    def __repr__(self):
        return f'<User {self.fullName}>'
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = User.hash_password(kwargs.get('password', ''))

    @classmethod
    def hash_password(cls, password):
        if password:
            return generate_password_hash(password)

        return None

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def find_by_email(cls, email):
        print(email)
        user = cls.query.filter(cls.email == email).first()
        return user

    def encode_auth_token(self, id):
        """Generates the auth token"""
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')
                ),
                'iat': datetime.utcnow(),
                'sub': {
                    'id': id,
                }
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(token):
        """
        Decodes the auth token

        :param string: token
        :return dict: The user's identity
        """
        try:
            payload = jwt.decode(
                token,
                current_app.config.get('SECRET_KEY'),
                algorithms='HS256'
            )
            return payload.get('sub')
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def add_to_wishlist(self, product):
        if not self.is_in_wishlist(product):
            self.wishlist.append(product)

    def remove_from_wishlist(self, product):
        if self.is_in_wishlist(product):
            self.wishlist.remove(product)

    def is_in_wishlist(self, product):
        return self.wishlist.filter(user_wishlist.c.product_id == product.id).count() > 0

# user_orders = db.Table('orders',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True)
# )
