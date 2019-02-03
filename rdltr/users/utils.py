import re
from functools import wraps

from flask import jsonify, request

from .model import User


def is_valid_email(email):
    mail_pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(mail_pattern, email) is not None


def register_controls(username, email, password, password_conf):
    ret = ''
    if not 2 < len(username) < 13:
        ret += 'Username: 3 to 12 characters required.\n'
    if not is_valid_email(email):
        ret += 'Valid email must be provided.\n'
    ret += passwords_controls(password, password_conf)
    return ret


def passwords_controls(password, password_conf):
    ret = ''
    if password != password_conf:
        ret += 'Password and password confirmation don\'t match.\n'
    if len(password) < 8:
        ret += 'Password: 8 characters required.\n'
    return ret


def verify_user(current_request):
    response_object = {
        'status': 'error',
        'message': 'Something went wrong. Please contact us.',
    }
    code = 401
    auth_header = current_request.headers.get('Authorization')
    if not auth_header:
        response_object['message'] = 'Provide a valid auth token.'
        return response_object, code, None
    auth_token = auth_header.split(" ")[1]
    resp = User.decode_auth_token(auth_token)
    if isinstance(resp, str):
        response_object['message'] = resp
        return response_object, code, None
    user = User.query.filter_by(id=resp).first()
    if not user:
        return response_object, code, None
    return None, None, resp


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object, code, resp = verify_user(request)
        if response_object:
            return jsonify(response_object), code
        return f(resp, *args, **kwargs)

    return decorated_function
