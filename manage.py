import os
import pytest
from flask_script import Manager
from app.create_app import create_app
from app.migrations.db import db
from dotenv import load_dotenv

load_dotenv()


app = create_app('development')
manager = Manager(app)


@manager.command
def test():
    os.environ['APP_SETTINGS'] = 'TESTING'
    pytest.main(['-v', '--cov=tests'])


@manager.command
def run():
    app.run()


if __name__ == '__main__':
    manager.run()
