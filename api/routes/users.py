from sqlalchemy import exc
from flask import current_app, jsonify, request, Blueprint

from api import db
from api.lib.decorators import authenticate
from api.errors import bad_request, server_error, not_found
from api.models import Product
from api.schema import ProductSchema

users = Blueprint('users', __name__, url_prefix='/api/users')

@users.route('/ping')
def ping():
    return {"message": "Users Route!"}


@users.route('/wishlist', methods=['GET'])
@authenticate
def get_wishlist(user):
    try:
        wishlist = ProductSchema(many=True).dump(user.wishlist)
    except (exc.IntegrityError, ValueError):
        db.session.rollback()
        return server_error('Something went wrong, please try again.')
    else:
        return jsonify(wishlist)


@users.route('/wishlist', methods=['POST'])
@authenticate
def toggle_item_in_wishlist(user):
    product_id = request.args.get('pid', type=int)

    try:
        product = Product.find_by_id(product_id)

        if product is None:
            return not_found('That product does not exist')

        if user.is_in_wishlist(product):
            user.remove_from_wishlist(product)
        else:
            user.add_to_wishlist(product)
        user.save()
    except (exc.IntegrityError, ValueError):
        db.session.rollback()
        return server_error('Something went wrong, please try again.')
    else:
        return jsonify(ProductSchema(many=True).dump(user.wishlist))

