import os

from flask import request

from apps.users.models import AdminUser
from base.exception_handler.base_exception import APIException
from utils.generate_jwt_token import decode_jwt


def authenticate():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise APIException(message='Auth Token Missing', status_code=401)
    auth_token = auth_header.split("Bearer ")[-1]
    if not auth_token:
        raise APIException(message='Invalid Token', status_code=401)
    try:
        payload = decode_jwt(auth_token, os.getenv("JWT_SECRET"), audience="DITTO_ADMIN_USER")
        if payload.get("tokenType") != "ACCESS":
            raise APIException(message='Invalid Token', status_code=401)
        user = AdminUser.query.filter_by(email=payload.get("email")).first()
        if not user:
            raise APIException(message="User not found", status_code=404)
        return user
    except Exception as e:
        raise APIException(message='Invalid Token', status_code=401)


def require_admin_authentication(func):
    def wrapper(*args, **kwargs):
        admin_user = authenticate()
        return func(admin_user=admin_user, *args, **kwargs)

    return wrapper
