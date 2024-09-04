import time
from datetime import timedelta, datetime

import jwt


def decode_jwt(encoded_jwt, secret, audience="DITTO_ADMIN_USER"):
    """"""
    return jwt.decode(encoded_jwt, secret, algorithms=["HS256"], audience=audience)


def encode_jwt(payload, secret, exp, token_type, aud="DITTO_ADMIN_USER", iss="DITTO"):
    """"""
    payload.update({"iss": iss,
                    "iat": int(time.time()),
                    "exp": exp,
                    "aud": aud,
                    "tokenType": token_type
                    })
    return jwt.encode(payload, secret, algorithm="HS256")


def generate_access_refresh_token(payload, secret, aud="DITTO_ADMIN_USER", iss="DITTO"):
    """"""
    access_token_exp = datetime.now() + timedelta(minutes=30)
    refresh_token_time = datetime.now() + timedelta(days=45)
    access_token = encode_jwt(payload, secret, time.mktime(access_token_exp.timetuple()), "ACCESS", aud, iss)
    refresh_token = encode_jwt(payload, secret, time.mktime(refresh_token_time.timetuple()), "REFRESH", aud, iss)
    return access_token, refresh_token, time.mktime(access_token_exp.timetuple())
