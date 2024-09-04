from datetime import datetime

from apps.users.models import AdminUser, OTPLog
from apps.users.utils import generate_otp_with_expiry
from apps.users.utils import send_otp_email
from base.exception_handler.base_exception import APIException
from base.views.base import BaseView
from databases.extensions import db


class SendOtpView(BaseView):
    def post(self, *args, **kwargs):
        try:
            data = self.request_data
            user = AdminUser.query.filter_by(email=data.get("email")).first()
            if not user:
                raise APIException(message="User not found", status_code=404)
            otp_code, expires_at = generate_otp_with_expiry(4, 15)
            otp_log = OTPLog.query.filter_by(email=data.get("email")).first()
            if otp_log:
                otp_log.otp = otp_code
                otp_log.expires_at = expires_at
                otp_log.updated_at = datetime.utcnow()
            else:
                otp_log = OTPLog(
                    email=data.get("email"),
                    otp=otp_code,
                    expires_at=expires_at,
                )
                db.session.add(otp_log)
            db.session.commit()
            send_otp_email(to_address=data.get("email"), otp_code=otp_code)
        except APIException:
            raise
        except Exception as e:
            from server import ditto_app_logger as logger
            logger.exception(short_message='Error Sending OTP', exception=e)
            raise APIException(message=str(e))
        return self.get_response({"message": "Otp sent to email"}, 200)
