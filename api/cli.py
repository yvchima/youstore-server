from datetime import datetime
import json
import random
import requests
import click
from sqlalchemy import exc, and_

from api import db as _db
from api.models import User, Product, Merchant
from data.merchant import merchants
from data.product import category, descriptions

def random_timestamp(start, end):
    return random.random() * (end - start) + start

def random_banner():
    colors = ["c7aae3", "364f6b", "17b978", "f85959", "e6c073", "589acc", "cc5ca5", "76cc5a"]
    return f'https://dummyimage.com/1344x400/{random.choice(colors)}/fff.png&text=Your+banner+goes+here,+click+to+edit.'

def random_image(data):
    return random.choice(data).get('image')

def gen_product_props():
    cat = random.choice(category)
    k = random.randrange(0, 4) if len(cat['colors']) > 3 else len(cat['colors'])
    return {
        'category': cat['name'],
        'sub_category': random.choice(cat['sub']),
        'colors': random.sample(cat['colors'], k=k),
        'sizes': cat['sizes'],
        'price': random.randrange(500, 200000)
    }

def register(app):
    @app.cli.group()
    def seed():
        """Database tables seed commands."""
        pass


    @seed.command()
    def db():
        """Seeds the database."""
        _db.drop_all()
        _db.create_all()
        _db.session.commit()

        merchants_table()
        product(999)
        users(20)

    # @seed.command()
    def merchants_table():
        """Seed the database with 20 Merchants."""
        try:
            print('Generating merchant data...')
            merchant_list = []
            data = requests.get('https://randomuser.me/api/?'
                f'results=20&inc=picture').json()

            for merchant in merchants:
                m = Merchant()
                m.store_name = merchant['store_name']
                m.store_location = f"{merchant['location']} {merchant['city']}"
                m.slug = m.gen_slug(m.store_name)
                m.store_photo = random.choice(data.get('results'))['picture']['medium']
                m.store_banner = random_banner()
                m.fullName = merchant['full_name']
                m.email = merchant['email']
                m.phone = merchant['phone']
                m.created_on = random_timestamp(
                    datetime(2021, 8, 1), datetime(2021, 12, 28))
                
                merchant_list.append(m)
            print('Saving to database...')
            _db.session.add_all(merchant_list)
            _db.session.commit()
        except exc.IntegrityError as error:
            _db.session.rollback()
            print(f'Error: {error}')


    # @seed.command()
    @click.argument('num_products')
    def product(num_products):
        """Seed the database with products. Default is 999."""
        print('Generating products data...')
        try:
            data = requests.get('https://fakestoreapi.com/products').json()
            merchants = Merchant.query.all()
            products = []

            for p in range(int(num_products)):
                images = [random_banner() for i in range(5)]
                images.append(random_image(data))
                prod = gen_product_props()
                merchant = random.choice(merchants)
                
                product = Product()
                product.name = random.choice(data).get('title')
                product.slug = product.gen_slug(product.name)
                product.price = prod['price']
                product.colors = json.dumps(prod['colors'])
                product.sizes = json.dumps(prod['sizes'])
                product.images = json.dumps(images) 
                product.description = f"{data[p%20].get('description')} {descriptions[random.randrange(1, 5)]}"
                product.inventory = random.randrange(0, 200)
                product.category = prod['category']
                product.sub_category = prod['sub_category']
                product.discount = random.randrange(0, 50) / 100
                product.created_at = random_timestamp(
                    datetime(2022, 12, 1), datetime(2022, 2, 20))
                product.merchant_id = merchant.id
                products.append(product)

            print('Saving to database...')
            _db.session.add_all(products)
            _db.session.commit()

        except exc.IntegrityError as error:
            _db.session.rollback()
            print(f'Error: {error}')

    # @seed.command()
    @click.argument('size')
    def users(size):
        """Seed the database with users.."""
        print('Generating users data...')
        try:
            data = requests.get('https://randomuser.me/api/?'
                f'results={size}&inc=name,email,picture,phone,location,nat'
            ).json()
            users = []
            products = Product.query.all()

            for user in data.get('results'):
                u = User(password='password')
                u.firstName = user.get('name')['first']
                u.lastName = user.get('name')['last']
                u.email = user.get('email')
                u.phone = user.get('phone')
                u.address = f"{user.get('location')['street']['number']} {user.get('location')['street']['name']} {user.get('location')['city']} {user.get('location')['state']}"
                u.photo = user.get('picture')['medium']
                u.created_on = random_timestamp(
                    datetime(2021, 8, 1), datetime(2021, 12, 28))
                u.wishlist.extend(random.sample(products, k=random.randrange(0, 15)))
                
                users.append(u)
            print('Saving to database...')
            _db.session.add_all(users)
            _db.session.commit()
        except exc.IntegrityError as error:
            _db.session.rollback()
            print(f'Error: {error}')
