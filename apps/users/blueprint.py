from flask import Blueprint

from apps.users.views import *

users_blueprint = Blueprint('users', __name__)

users_blueprint.add_url_rule('users/login/', view_func=UserLoginAPIView.as_view('login_api'))
users_blueprint.add_url_rule('users/send-otp/', view_func=SendOtpView.as_view('send_otp_api'))
