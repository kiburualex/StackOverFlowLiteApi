from flask_api import FlaskAPI
# local import
# from app.configuration import settings
import settings


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = settings.SECRET

    """ Flask-Restplus settings """
    SWAGGER_UI_DOC_EXPANSION = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    RESTPLUS_VALIDATE = settings.RESTPLUS_VALIDATE
    RESTPLUS_MASK_SWAGGER = settings.RESTPLUS_MASK_SWAGGER
    ERROR_404_HELP = settings.RESTPLUS_ERROR_404_HELP


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}


def create_app(config_name):
    """Create a flask app instance."""
    app = FlaskAPI(__name__)
    app.config.from_object(app_config[config_name])
    app.url_map.strict_slashes = False

    return app
