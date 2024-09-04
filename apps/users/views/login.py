import os
from datetime import datetime

from apps.users.models import OTPLog
from base.exception_handler.base_exception import APIException
from base.views.base import BaseView
from databases.extensions import db
from utils.generate_jwt_token import generate_access_refresh_token


class UserLoginAPIView(BaseView):
    def post(self, *args, **kwargs):
        data = self.request_data
        otp_log = OTPLog.query.filter_by(email=data.get("email")).first()
        if not otp_log or int(otp_log.otp) != int(data.get("otp")) or otp_log.expires_at < datetime.utcnow():
            raise APIException(message="Invalid OTP", status_code=401)
        access_token, _, eat = generate_access_refresh_token({"email": data.get("email")}, os.getenv("JWT_SECRET"))
        db.session.delete(otp_log)
        db.session.commit()
        return self.get_response({"access_token": access_token, "expires_at": eat}, 200)
