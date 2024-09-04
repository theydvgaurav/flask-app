from pathlib import Path

from flask import Flask, jsonify
from flask_cors import CORS

from apps.policies.blueprint import policy_blueprint
from apps.users.blueprint import users_blueprint
from base.celery import celery_init_app
from base.exception_handler.base_exception import APIException
from common.logging.logger import DittoAppLogger
from databases.config import Config
from databases.extensions import db, migrate
from utils.celery_config import CELERY_CONFIG

config_path = Path(__file__).with_name("logging_conf.json")
ditto_app_logger = DittoAppLogger.make_logger(config_path)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    app.config.update(
        CELERY=CELERY_CONFIG
    )
    app.register_blueprint(users_blueprint, url_prefix='/v1')
    app.register_blueprint(policy_blueprint, url_prefix='/v1')

    @app.errorhandler(Exception)
    def handle_exception(error):
        response = jsonify(str(repr(error)))
        response.status_code = 500
        return response

    @app.errorhandler(APIException)
    def handle_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    return app


flask_app = create_app()
celery_app = celery_init_app(flask_app)
