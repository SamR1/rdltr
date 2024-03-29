import os
from argparse import Namespace
from typing import Generator
from unittest.mock import Mock

import pytest
from flask import Flask, Request
from werkzeug.test import TestResponse

from .. import create_app, db
from ..articles.model import Article, Category, Tag
from ..users.model import User
from .utils_mock_server import MockTestServer
from .utils_requests import (
    mock_api,
    mock_response_different_encoding,
    mock_response_empty,
    mock_response_not_found,
    mock_response_ok,
)

os.environ["FLASK_ENV"] = "testing"
os.environ["RDLTR_SETTINGS"] = "rdltr.config.TestingConfig"
os.environ["RDLTR_ALLOW_REGISTRATION"] = "true"
TestResponse.__test__ = False  # type: ignore


@pytest.fixture
def app() -> Generator:
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
    return app


@pytest.fixture
def app_wo_db() -> Flask:
    app = create_app()
    return app


@pytest.fixture
def app_no_registration() -> Generator:
    app = create_app()
    app.config["REGISTRATION_ALLOWED"] = False
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
    return app


@pytest.fixture()
def user_1() -> User:
    user = User(username="test", email="test@test.com", password="12345678")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def user_2() -> User:
    user = User(username="toto", email="toto@example.com", password="87654321")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def cat_1(user_1: User) -> Category:
    cat = Category(name="python", user_id=user_1.id)
    db.session.add(cat)
    db.session.commit()
    return cat


@pytest.fixture()
def cat_2(user_2: User) -> Category:
    cat = Category(name="moto", user_id=user_2.id)
    cat.description = "related to motorcycles"
    db.session.add(cat)
    db.session.commit()
    return cat


@pytest.fixture()
def cat_3(user_1: User) -> Category:
    cat = Category(name="python", user_id=user_1.id)
    cat.is_default = True
    db.session.add(cat)
    db.session.commit()
    return cat


@pytest.fixture()
def cat_4(user_1: User) -> Category:
    cat = Category(name="moto", user_id=user_1.id)
    db.session.add(cat)
    db.session.commit()
    return cat


@pytest.fixture()
def tag_1(user_1: User) -> Tag:
    tag = Tag(name="tips", user_id=user_1.id)
    db.session.add(tag)
    db.session.commit()
    return tag


@pytest.fixture()
def tag_2(user_1: User) -> Tag:
    tag = Tag(name="tuto", user_id=user_1.id)
    db.session.add(tag)
    db.session.commit()
    return tag


@pytest.fixture()
def tag_3(user_2: User) -> Tag:
    tag = Tag(name="moto", user_id=user_2.id)
    db.session.add(tag)
    db.session.commit()
    return tag


@pytest.fixture()
def tag_4(user_1: User) -> Tag:
    tag = Tag(name="new", user_id=user_1.id)
    db.session.add(tag)
    db.session.commit()
    return tag


@pytest.fixture()
def article_1(cat_1: Category, tag_1: Tag, tag_2: Tag) -> Article:
    article = Article(
        category_id=cat_1.id,
        url="https://test.com",
        title="Python tips",
        content="Test",
        html_content="<html><head><title>Titre</head>"
        "<body><p>Test</p></body></html>",
    )
    article.tags.append(tag_1)
    article.tags.append(tag_2)
    db.session.add(article)
    db.session.commit()
    return article


@pytest.fixture()
def article_2(cat_1: Category) -> Article:
    article = Article(
        category_id=cat_1.id,
        url="https://test.com",
        title="Another article",
        content="Test2",
        html_content="<html><head><title>Titre2</head>"
        "<body><p>Test2</p></body></html>",
    )
    article.comments = "just a comment"
    article.read_status = True
    article.favorite = True
    db.session.add(article)
    db.session.commit()
    return article


@pytest.fixture()
def article_3(cat_2: Category) -> Article:
    article = Article(
        category_id=cat_2.id,
        url="https://test.com",
        title="Another article",
        content="Test3",
        html_content="<html><head><title>Titre3</head>"
        "<body><p>Test3</p></body></html>",
    )
    article.comments = "just a comment"
    db.session.add(article)
    db.session.commit()
    return article


@pytest.fixture()
def article_4(cat_4: Category) -> Article:
    article = Article(
        category_id=cat_4.id,
        url="https://test.com",
        title="Great article",
        content="Test4",
        html_content="<html><head><title>Titre4</head>"
        "<body><p>Test4</p></body></html>",
    )
    article.comments = "just a comment"
    db.session.add(article)
    db.session.commit()
    return article


@pytest.fixture()
def articles_20(cat_1: Category) -> None:
    for n in range(1, 21):
        article = Article(
            category_id=cat_1.id,
            url="https://python.com",
            title=f"Python article {n}",
            content=f"Test{n}",
            html_content=f"<html><head><title>Titre{n}</head>"
            f"<body><p>Test{n}</p></body></html>",
        )
        db.session.add(article)
    db.session.commit()


@pytest.fixture()
def mock_request_ok() -> Mock:
    return mock_api(mock_response_ok)


@pytest.fixture()
def mock_request_not_found() -> Mock:
    return mock_api(mock_response_not_found)


@pytest.fixture()
def mock_request_empty() -> Mock:
    return mock_api(mock_response_empty)


@pytest.fixture()
def mock_request_different_encoding() -> Mock:
    return mock_api(mock_response_different_encoding)


@pytest.fixture
def mock_server(request: Request) -> Generator:
    server = MockTestServer()
    server.start()
    yield server
    server.close_session()


@pytest.fixture
def firefox_options(firefox_options: Namespace) -> Namespace:
    firefox_options.add_argument("--headless")
    return firefox_options
