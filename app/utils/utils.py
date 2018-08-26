from urllib.parse import urlparse
import os
import re
from config import BaseConfig


def db_config(database_uri):

    """
        This function extracts postgres url
        and return database login information
        :param database_uri: database Configuration uri
        :return: database login information
    """

    if os.environ.get('DATABASE_URL'):
        database_uri = os.environ.get('DATABASE_URL')

    result = urlparse(database_uri)
    config = {
        'database': result.path[1:],
        'user': result.username,
        'password': result.password,
        'host': result.hostname
    }

    """ Determines which database to use """
    if os.environ.get('APP_SETTINGS') == 'TESTING':
        config['database'] = BaseConfig.TEST_DB
    return config


def valid_email(email):

    """  Validate email """

    return re.match(r'^.+@([?)[a-zA-Z0-9-.])+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$', email)

