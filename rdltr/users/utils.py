import re
from functools import wraps
from typing import Any, Callable, Dict, Optional, Tuple, Union

from flask import Request, request

from .model import User


def is_valid_email(email: str) -> bool:
    mail_pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(mail_pattern, email) is not None


def register_controls(
    username: str, email: str, password: str, password_conf: str
) -> str:
    ret = ""
    if not 2 < len(username) < 13:
        ret += "Username: 3 to 12 characters required.\n"
    if not is_valid_email(email):
        ret += "Valid email must be provided.\n"
    ret += passwords_controls(password, password_conf)
    return ret


def passwords_controls(password: str, password_conf: str) -> str:
    ret = ""
    if password != password_conf:
        ret += "Password and password confirmation don't match.\n"
    if len(password) < 8:
        ret += "Password: 8 characters required.\n"
    return ret


def verify_user(
    current_request: Request,
) -> Tuple[Optional[Dict], Optional[int], Optional[int]]:
    response_object = {
        "status": "error",
        "message": "Something went wrong. Please contact us.",
    }
    code = 401
    auth_header = current_request.headers.get("Authorization")
    if not auth_header:
        response_object["message"] = "Provide a valid auth token."
        return response_object, code, None
    auth_token = auth_header.split(" ")[1]
    user_id = User.decode_auth_token(auth_token)
    if isinstance(user_id, str):
        response_object["message"] = user_id
        return response_object, code, None
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return response_object, code, None
    return None, None, user_id


def authenticate(f: Callable) -> Callable:
    @wraps(f)
    def decorated_function(
        *args: Any, **kwargs: Any
    ) -> Union[Callable, Tuple[Dict, Optional[int]]]:
        response_object, code, user_id = verify_user(request)
        if response_object:
            return response_object, code
        return f(user_id, *args, **kwargs)

    return decorated_function
