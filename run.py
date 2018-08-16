from flask import request, jsonify, abort, Blueprint
# local import
from app.api.v1 import api
from app.api.v1.question import ns as questions_namespace
from app.api.v1.user import ns as users_namespace
from app.configuration.config import create_app
from app.configuration import settings

config_name = settings.APP_ENVIRONMENT_SETTINGS # config_name = "development"
app = create_app(config_name)

api.init_app(app)
api.add_namespace(questions_namespace)
api.add_namespace(users_namespace)


if __name__ == '__main__':
	app.run()
