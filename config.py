import settings
import os


class BaseConfig(object):

    """
        Base Configuration for the Entire App
    """

    basedir = os.path.abspath(os.path.dirname(__file__))
    DATABASE_URI = "postgresql://stack:stack@127.0.0.1:5432/stack"
    TEST_DB = 'test_db'
    DEBUG = True
    SECRET_KEY = '\xbf\xb0\x11\xb1\xcd\xf9\xba\x8bp\x0c...'

    """ Flask-Restplus settings """
    SWAGGER_UI_DOC_EXPANSION = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    RESTPLUS_VALIDATE = settings.RESTPLUS_VALIDATE
    RESTPLUS_MASK_SWAGGER = settings.RESTPLUS_MASK_SWAGGER
    ERROR_404_HELP = settings.RESTPLUS_ERROR_404_HELP


class DevelopmentConfig(BaseConfig):

    """
        Development Environment Configuration
    """

    DEBUG = True


class TestingConfig(BaseConfig):

    """
        Testing Environment Configuration
    """

    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):

    """
        Production Environment Configuration
    """

    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}

key = BaseConfig.SECRET_KEY
