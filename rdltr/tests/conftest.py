import os

import pytest

from .. import create_app, db
from ..articles.model import Article, Category, Tag
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


@pytest.fixture
def app_wo_db():
    app = create_app()
    return app


@pytest.fixture()
def user_1():
    user = User(username='test', email='test@test.com', password='12345678')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def user_2():
    user = User(username='toto', email='toto@example.com', password='87654321')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def cat_1(user_1):
    cat = Category(name='python', user_id=user_1.id)
    db.session.add(cat)
    db.session.commit()
    return cat


@pytest.fixture()
def cat_2(user_2):
    cat = Category(
        description='related to motorcycles', name='moto', user_id=user_2.id
    )
    db.session.add(cat)
    db.session.commit()
    return cat


@pytest.fixture()
def tag_1(user_1):
    cat = Tag(name='tips', user_id=user_1.id)
    db.session.add(cat)
    db.session.commit()
    return cat


@pytest.fixture()
def tag_2(user_1):
    cat = Tag(name='tuto', user_id=user_1.id)
    cat.color = 'red'
    db.session.add(cat)
    db.session.commit()
    return cat


@pytest.fixture()
def article_1(cat_1, tag_1, tag_2):
    article = Article(
        category_id=cat_1.id, title='Python tips', content='<html></html>'
    )
    article.tags.append(tag_1)
    article.tags.append(tag_2)
    db.session.add(article)
    db.session.commit()
    return article


@pytest.fixture()
def article_2(cat_1):
    article = Article(
        category_id=cat_1.id, title='Another article', content='<html></html>'
    )
    article.comments = 'just a comment'
    db.session.add(article)
    db.session.commit()
    return article
