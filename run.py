import os
import pytest
from flask_script import Manager
from app.create_app import create_app
from app.migrations.db import db

app = create_app('development')
manager = Manager(app)


@manager.command
def test():
    os.environ['APP_SETTINGS'] = 'TESTING'
    db.migrate_test_db()
    pytest.main(['-v', '--cov=tests'])
    db.drop_test_database()

@manager.command
def run():
    app.run()


if __name__ == '__main__':
    manager.run()
