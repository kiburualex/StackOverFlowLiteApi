from flask_api import FlaskAPI
from config import app_config
from app.api.v1 import api
from app.api.v1.question import ns as questions_namespace
from app.api.v1.user import ns as users_namespace
from app.api.v1.answer import ns as answers_namespace
from app.migrations.db import db


def create_app(config_name):
    """Create a flask app instance."""
    app = FlaskAPI(__name__)
    app.config.from_object(app_config[config_name])
    app.url_map.strict_slashes = False

    api.init_app(app)
    api.add_namespace(questions_namespace)
    api.add_namespace(answers_namespace)
    api.add_namespace(users_namespace)

    """ run the database migrations for the main application """
    db.migrate()

    return app
