import os

import pytest

from .. import create_app, db
from ..users.model import User

os.environ["FLASK_ENV"] = 'testing'
os.environ["APP_SETTINGS"] = 'rdltr.config.TestingConfig'


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
    return app


@pytest.fixture()
def user_1():
    user = User(username='test', email='test@test.com', password='12345678')
    db.session.add(user)
    db.session.commit()
    return user
