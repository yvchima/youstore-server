from math import prod
from unicodedata import category
from sqlalchemy import exc
from flask import current_app, jsonify, request, Blueprint, url_for

from api import db
from api.lib.decorators import authenticate
from api.errors import bad_request, server_error, not_found
from api.models import Product
from api.schema import ProductSchema

products = Blueprint('products', __name__, url_prefix='/api/products')

@products.route('/ping')
def ping():
    return {"message": "Products Route!"}


@products.route('', methods=['GET'])
def get_products():
    category = request.args.get('category')
    page = request.args.get('page', 1, type=int)

    try:
        products = Product.query.filter(Product.category==category).order_by(
            Product.created_on.desc()).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('products.get_products', page=products.next_num, category=category) \
        if products.has_next else None
        prev_url = url_for('products.get_products', page=products.prev_num, category=category) \
        if products.has_prev else None
    except (exc.IntegrityError, ValueError):
        db.session.rollback()
        return server_error('Something went wrong, please try again.')
    else:
        data = {
            'items': ProductSchema(many=True).dump(products.items),
            'meta': {
                "page": page,
                "per_page": current_app.config['POSTS_PER_PAGE'],
                "total_pages": products.pages,
                "total_items": products.total,
            },
            '_links': {
                "next": next_url,
                "prev": prev_url,
            }
        }
        return jsonify(data)


@products.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.filter_by(id=product_id).first()

        if product is None:
            return not_found('That product does not exist')

    except (exc.IntegrityError, ValueError):
        db.session.rollback()
        return server_error('Something went wrong, please try again.')
    else:
        return jsonify(ProductSchema().dump(product))