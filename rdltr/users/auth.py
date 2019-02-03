from flask import Blueprint, jsonify, request
from sqlalchemy import exc, or_

from .. import app_log, bcrypt, db
from .model import User
from .utils import authenticate, register_controls

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    # get post data
    post_data = request.get_json()
    if (
        not post_data
        or post_data.get('username') is None
        or post_data.get('email') is None
        or post_data.get('password') is None
        or post_data.get('password_conf') is None
    ):
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    password_conf = post_data.get('password_conf')

    try:
        ret = register_controls(username, email, password, password_conf)
    except TypeError as e:
        app_log.error(e)

        response_object = {
            'status': 'error',
            'message': 'Error. Please try again or contact the administrator.',
        }
        return jsonify(response_object), 500
    if ret != '':
        response_object = {'status': 'error', 'message': 'Errors: ' + ret}
        return jsonify(response_object), 400

    try:
        # check for existing user
        user = User.query.filter(
            or_(User.username == username, User.email == email)
        ).first()
        if not user:
            # add new user to db
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            # generate auth token
            auth_token = new_user.encode_auth_token(new_user.id)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode(),
                'user': new_user.serialize(),
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'error',
                'message': 'Sorry. That user already exists.',
            }
            return jsonify(response_object), 400
    # handler errors
    except (exc.IntegrityError, exc.OperationalError, ValueError) as e:
        db.session.rollback()
        app_log.error(e)

        response_object = {
            'status': 'error',
            'message': 'Error. Please try again or contact the administrator.',
        }
        return jsonify(response_object), 500


@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    # get post data
    post_data = request.get_json()
    if not post_data:
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        # check for existing user
        user = User.query.filter(User.email == email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # generate auth token
            auth_token = user.encode_auth_token(user.id)
            response_object = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'auth_token': auth_token.decode(),
                'user': user.serialize(),
            }
            return jsonify(response_object), 200
        else:
            response_object = {
                'status': 'error',
                'message': 'Invalid credentials.',
            }
            return jsonify(response_object), 404
    # handler errors
    except (exc.IntegrityError, exc.OperationalError, ValueError) as e:
        db.session.rollback()
        app_log.error(e)
        response_object = {
            'status': 'error',
            'message': 'Error. Please try again or contact the administrator.',
        }
        return jsonify(response_object), 500


@auth_blueprint.route('/auth/logout', methods=['GET'])
@authenticate
def logout_user(user_id):
    # all checks are made by @authenticate
    response_object = {
        'status': 'success',
        'message': 'Successfully logged out.',
    }
    return jsonify(response_object), 200


@auth_blueprint.route('/auth/profile', methods=['GET'])
@authenticate
def get_user_status(user_id):
    user = User.query.filter_by(id=user_id).first()
    response_object = {'status': 'success', 'user': user.serialize()}
    return jsonify(response_object), 200
