from sqlalchemy import exc
from marshmallow import ValidationError
from flask import jsonify, request, url_for, Blueprint

from api import db
from api.schema import AuthSchema, UserSchema
from api.models import User
from api.lib.decorators import authenticate
from api.errors import error_response, bad_request, server_error

auth = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth.route('/ping')
def ping():
    return {"message": "Auth Route!"}


@auth.route('/register', methods=['POST'])
def register_user():
    post_data = request.get_json()

    if not post_data:
        return bad_request("No input data provided")

    try:
        data = AuthSchema().load(post_data)
    except ValidationError as err:
        return error_response(422, err.messages)

    email = data.get('email')

    # check for existing user
    user = User.find_by_email(data.get('email'))

    if user:
        return bad_request('That user already exists.')

    user = User()
    user.email = email
    user.firstName = data.get('firstName')
    user.lastName = data.get('lastName')
    user.phone = data.get('phone')
    user.password = data.get('password')

    try:
        user.save()
    except (exc.IntegrityError, ValueError):
        db.session.rollback()
        return server_error('Something went wrong, please try again.')

    response = jsonify({
        'token': user.encode_auth_token(user.id),
        'user': UserSchema().dump(user)
    })
    response.status_code = 201
    response.headers['Location'] = url_for('auth.get_user', id=user.id)
    return response


@auth.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    print(data)

    if data is None:
        return bad_request("No input data provided")

    try:
        # check for existing user
        user = User.find_by_email(data.get('email'))

        if user and user.check_password(data.get('password')):
            return jsonify({
                'token': user.encode_auth_token(user.id),
                'user': UserSchema().dump(user)
            })
        else:
            return error_response(401, 'Incorrect email or password.')
    except Exception:
        return server_error('Something went wrong, please try again.')


@auth.route('/logout', methods=['GET'])
@authenticate
def logout_user(user):
    return jsonify({'message': 'Successfully logged out.'})


@auth.route('/user', methods=['GET'])
@authenticate
def get_user(user):
    return jsonify({'user': UserSchema().dump(user)})
