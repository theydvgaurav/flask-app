from flask import jsonify, make_response, request
from flask.views import MethodView

from base.exception_handler.base_exception import APIException


class BaseView(MethodView):

    @property
    def request_data(self):
        return request.json

    @staticmethod
    def get_response(data=None, status_code=200):
        if not data:
            return make_response(jsonify(''), 204)
        return make_response(jsonify(data), status_code)

    @staticmethod
    def get_validated_data(validation_class, data, **kwargs):
        try:
            return validation_class(**data).dict(**kwargs)
        except Exception as e:
            raise APIException(message=str(e), status_code=400)
