import json

from flask import Flask
from werkzeug.test import TestResponse

from rdltr.articles.model import Article, Category
from rdltr.tests.utils import check_400_invalid_payload
from rdltr.users.model import User


def check_404_category(response: "TestResponse") -> None:
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data["status"] == "not found"
    assert data["message"] == "Category not found."


def test_get_no_categories(app: Flask, user_1: User) -> None:
    client = app.test_client()
    resp_login = client.post(
        "/api/auth/login",
        data=json.dumps(dict(email="test@test.com", password="12345678")),
        content_type="application/json",
    )
    response = client.get(
        "/api/categories",
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == "success"
    assert data["data"] == []


def test_get_one_category(app: Flask, user_1: User, cat_1: Category) -> None:
    client = app.test_client()
    resp_login = client.post(
        "/api/auth/login",
        data=json.dumps(dict(email="test@test.com", password="12345678")),
        content_type="application/json",
    )
    response = client.get(
        "/api/categories",
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == "success"
    assert len(data["data"]) == 1
    assert data["data"][0]["id"] == 1
    assert data["data"][0]["user_id"] == 1
    assert data["data"][0]["name"] == "python"
    assert data["data"][0]["is_default"] is False
    assert data["data"][0]["nb_articles"] == 0


def test_add_category_minimal_payload(app: Flask, user_1: User) -> None:
    client = app.test_client()
    resp_login = client.post(
        "/api/auth/login",
        data=json.dumps(dict(email="test@test.com", password="12345678")),
        content_type="application/json",
    )
    response = client.post(
        "/api/categories",
        data=json.dumps(dict(name="Moto")),
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
        content_type="application/json",
    )
    assert response.status_code == 201
    data = json.loads(response.data.decode())
    assert data["status"] == "success"
    assert len(data["data"]) == 1
    assert data["data"][0]["id"] == 1
    assert data["data"][0]["user_id"] == 1
    assert data["data"][0]["name"] == "moto"
    assert not data["data"][0]["description"]
    assert data["data"][0]["is_default"] is False
    assert data["data"][0]["nb_articles"] == 0

    response = client.get(
        "/api/auth/profile",
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data["status"] == "success"
    assert data["user"] is not None
    assert data["user"]["username"] == "test"
    assert data["user"]["email"] == "test@test.com"
    assert data["user"]["created_at"]
    assert data["user"]["categories"][0]["id"] == 1
    assert data["user"]["categories"][0]["user_id"] == 1
    assert data["user"]["categories"][0]["name"] == "moto"
    assert data["user"]["categories"][0]["nb_articles"] == 0
    assert data["user"]["tags"] == []


def test_add_category_full_payload(app: Flask, user_1: User) -> None:
    client = app.test_client()
    resp_login = client.post(
        "/api/auth/login",
        data=json.dumps(dict(email="test@test.com", password="12345678")),
        content_type="application/json",
    )
    response = client.post(
        "/api/categories",
        data=json.dumps(
            dict(name="moto", description="related to motorcycles")
        ),
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
        content_type="application/json",
    )
    assert response.status_code == 201
    data = json.loads(response.data.decode())
    assert data["status"] == "success"
    assert len(data["data"]) == 1
    assert data["data"][0]["id"] == 1
    assert data["data"][0]["user_id"] == 1
    assert data["data"][0]["name"] == "moto"
    assert data["data"][0]["description"] == "related to motorcycles"
    assert data["data"][0]["is_default"] is False
    assert data["data"][0]["nb_articles"] == 0


def test_add_category_invalid_payload(app: Flask, user_1: User) -> None:
    client = app.test_client()
    resp_login = client.post(
        "/api/auth/login",
        data=json.dumps(dict(email="test@test.com", password="12345678")),
        content_type="application/json",
    )
    response = client.post(
        "/api/categories",
        data=json.dumps(dict(description="related to motorcycles")),
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
        content_type="application/json",
    )
    check_400_invalid_payload(response)


def test_add_existing_category(
    app: Flask, user_1: User, cat_1: Category
) -> None:
    client = app.test_client()
    resp_login = client.post(
        "/api/auth/login",
        data=json.dumps(dict(email="test@test.com", password="12345678")),
        content_type="application/json",
    )
    response = client.post(
        "/api/categories",
        data=json.dumps(dict(name="python")),
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
        content_type="application/json",
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == "error"
    assert data["message"] == 'A category named "python" already exists.'


def test_add_another_user_existing_category(
    app: Flask, user_1: User, cat_2: Category
) -> None:
    client = app.test_client()
    resp_login = client.post(
        "/api/auth/login",
        data=json.dumps(dict(email="test@test.com", password="12345678")),
        content_type="application/json",
    )
    response = client.post(
        "/api/categories",
        data=json.dumps(dict(name="moto")),
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
        content_type="application/json",
    )
    assert response.status_code == 201
    data = json.loads(response.data.decode())
    assert data["status"] == "success"
    assert len(data["data"]) == 1
    assert data["data"][0]["id"] == 2
    assert data["data"][0]["user_id"] == 1
    assert data["data"][0]["name"] == "moto"
    assert data["data"][0]["is_default"] is False
    assert data["data"][0]["nb_articles"] == 0


def test_update_existing_category_minimal(
    app: Flask, user_1: User, cat_1: Category
) -> None:
    client = app.test_client()
    resp_login = client.post(
        "/api/auth/login",
        data=json.dumps(dict(email="test@test.com", password="12345678")),
        content_type="application/json",
    )
    response = client.patch(
        "/api/categories/1",
        data=json.dumps(dict(name="new label")),
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == "success"
    assert len(data["data"]) == 1
    assert data["data"][0]["id"] == 1
    assert data["data"][0]["user_id"] == 1
    assert data["data"][0]["name"] == "new label"
    assert data["data"][0]["description"] is None
    assert data["data"][0]["is_default"] is False
    assert data["data"][0]["nb_articles"] == 0


def test_update_existing_category(
    app: Flask, user_1: User, cat_1: Category
) -> None:
    client = app.test_client()
    resp_login = client.post(
        "/api/auth/login",
        data=json.dumps(dict(email="test@test.com", password="12345678")),
        content_type="application/json",
    )
    response = client.patch(
        "/api/categories/1",
        data=json.dumps(dict(name="new label", description="new description")),
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == "success"
    assert len(data["data"]) == 1
    assert data["data"][0]["id"] == 1
    assert data["data"][0]["user_id"] == 1
    assert data["data"][0]["name"] == "new label"
    assert data["data"][0]["description"] == "new description"
    assert data["data"][0]["is_default"] is False
    assert data["data"][0]["nb_articles"] == 0


def test_update_existing_category_name(
    app: Flask, user_1: User, cat_1: Category, cat_4: Category
) -> None:
    client = app.test_client()
    resp_login = client.post(
        "/api/auth/login",
        data=json.dumps(dict(email="test@test.com", password="12345678")),
        content_type="application/json",
    )
    response = client.patch(
        "/api/categories/1",
        data=json.dumps(dict(name="moto", description="new description")),
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
        content_type="application/json",
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == "error"
    assert data["message"] == 'A category named "moto" already exists.'


def test_update_another_user_category(
    app: Flask, user_1: User, cat_2: Category
) -> None:
    client = app.test_client()
    resp_login = client.post(
        "/api/auth/login",
        data=json.dumps(dict(email="test@test.com", password="12345678")),
        content_type="application/json",
    )
    response = client.patch(
        "/api/categories/1",
        data=json.dumps(dict(name="new label", description="new description")),
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
        content_type="application/json",
    )
    check_404_category(response)


def test_update_not_existing_category(app: Flask, user_1: User) -> None:
    client = app.test_client()
    resp_login = client.post(
        "/api/auth/login",
        data=json.dumps(dict(email="test@test.com", password="12345678")),
        content_type="application/json",
    )
    response = client.patch(
        "/api/categories/100",
        data=json.dumps(dict(name="new label", description="new description")),
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
        content_type="application/json",
    )
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data["status"] == "not found"
    assert data["message"] == "Category not found."


def test_update_category_invalid_payload(
    app: Flask, user_1: User, cat_1: Category
) -> None:
    client = app.test_client()
    resp_login = client.post(
        "/api/auth/login",
        data=json.dumps(dict(email="test@test.com", password="12345678")),
        content_type="application/json",
    )
    response = client.patch(
        "/api/categories/1",
        data=json.dumps(dict()),
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
        content_type="application/json",
    )
    check_400_invalid_payload(response)


def test_delete_category(app: Flask, user_1: User, cat_1: Category) -> None:
    client = app.test_client()
    resp_login = client.post(
        "/api/auth/login",
        data=json.dumps(dict(email="test@test.com", password="12345678")),
        content_type="application/json",
    )
    response = client.delete(
        "/api/categories/1",
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
        content_type="application/json",
    )
    assert response.status_code == 204


def test_delete_another_user_category(
    app: Flask, user_1: User, cat_2: Category
) -> None:
    client = app.test_client()
    resp_login = client.post(
        "/api/auth/login",
        data=json.dumps(dict(email="test@test.com", password="12345678")),
        content_type="application/json",
    )
    response = client.delete(
        "/api/categories/2",
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
        content_type="application/json",
    )
    check_404_category(response)


def test_delete_not_existing_category(app: Flask, user_1: User) -> None:
    client = app.test_client()
    resp_login = client.post(
        "/api/auth/login",
        data=json.dumps(dict(email="test@test.com", password="12345678")),
        content_type="application/json",
    )
    response = client.delete(
        "/api/categories/999",
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
        content_type="application/json",
    )
    check_404_category(response)


def test_delete_category_with_articles(
    app: Flask, cat_3: Category, article_4: Article
) -> None:
    client = app.test_client()
    resp_login = client.post(
        "/api/auth/login",
        data=json.dumps(dict(email="test@test.com", password="12345678")),
        content_type="application/json",
    )

    response = client.get(
        "/api/articles/1",
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == "success"
    assert len(data["data"]) == 1
    assert data["data"][0]["title"] == "Great article"
    assert data["data"][0]["category"]["id"] == 2
    assert data["data"][0]["category"]["name"] == "moto"
    assert data["data"][0]["category"]["nb_articles"] == 1

    response = client.delete(
        "/api/categories/2",
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
        content_type="application/json",
    )
    assert response.status_code == 204

    response = client.get(
        "/api/articles/1",
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == "success"
    assert len(data["data"]) == 1
    assert data["data"][0]["title"] == "Great article"
    assert data["data"][0]["category"]["id"] == 1
    assert data["data"][0]["category"]["name"] == "python"
    assert data["data"][0]["category"]["nb_articles"] == 1


def test_delete_default_category(app: Flask, cat_3: Category) -> None:
    client = app.test_client()
    resp_login = client.post(
        "/api/auth/login",
        data=json.dumps(dict(email="test@test.com", password="12345678")),
        content_type="application/json",
    )

    response = client.delete(
        "/api/categories/1",
        headers=dict(
            Authorization="Bearer "
            + json.loads(resp_login.data.decode())["auth_token"]
        ),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == "error"
    assert data["message"] == "Default category can not be deleted."
