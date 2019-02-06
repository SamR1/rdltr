import json
from unittest.mock import patch

from .utils import check_400_invalid_payload, check_500_error
from .utils_requests import html_doc_body_ok


def check_500_category_not_found(response):
    assert response.status_code == 500
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert data['message'] == 'Article category not found.'


def check_404_article_not_found(response):
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data['status'] == 'not found'
    assert data['message'] == 'Article not found.'


def test_get_no_articles(app, user_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.get(
        '/api/articles',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert data['data'] == []


def test_get_articles_one_result(app, article_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.get(
        '/api/articles',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 1
    assert data['data'][0]['title'] == 'Python tips'
    assert data['data'][0]['content'] == '<html></html>'
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert 'date_added' in data['data'][0]
    assert data['data'][0]['tags'][0]['name'] == 'tips'
    assert data['data'][0]['tags'][1]['color'] == 'red'


def test_get_articles(app, article_1, article_2, article_3):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.get(
        '/api/articles',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 2
    assert data['data'][0]['title'] == 'Python tips'
    assert data['data'][0]['content'] == '<html></html>'
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert 'date_added' in data['data'][0]
    assert data['data'][0]['tags'][0]['name'] == 'tips'
    assert data['data'][0]['tags'][1]['color'] == 'red'

    assert data['data'][1]['title'] == 'Another article'
    assert data['data'][1]['content'] == '<html></html>'
    assert data['data'][1]['url'] == 'https://test.com'
    assert data['data'][1]['comments'] == 'just a comment'
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert 'date_added' in data['data'][0]
    assert data['data'][1]['tags'] == []


def test_get_article(app, article_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.get(
        '/api/articles/1',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 1
    assert data['data'][0]['title'] == 'Python tips'
    assert data['data'][0]['content'] == '<html></html>'
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert 'date_added' in data['data'][0]
    assert data['data'][0]['tags'][0]['name'] == 'tips'
    assert data['data'][0]['tags'][1]['color'] == 'red'


def test_get_article_no_result(app, user_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.get(
        '/api/articles/1',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    check_404_article_not_found(response)


def test_get_article_no_result_another_user_article(app, user_1, article_3):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.get(
        '/api/articles/1',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    check_404_article_not_found(response)


@patch('requests.get')
def test_add_article_to_default_category_no_tags(
    get_mock, fake_request_ok, app, user_1, cat_3
):
    get_mock.return_value = fake_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/articles',
        data=json.dumps(dict(url='https://example.com')),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    assert response.status_code == 201
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 1
    assert data['data'][0]['title'] == 'this is a title'
    assert data['data'][0]['content'] == html_doc_body_ok
    assert data['data'][0]['url'] == 'https://example.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default']
    assert 'date_added' in data['data'][0]
    assert len(data['data'][0]['tags']) == 0


@patch('requests.get')
def test_add_article_to_category_no_tags(
    get_mock, fake_request_ok, app, user_1, cat_1
):
    get_mock.return_value = fake_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/articles',
        data=json.dumps(dict(url='https://example.com', category_id=1)),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    assert response.status_code == 201
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 1
    assert data['data'][0]['title'] == 'this is a title'
    assert data['data'][0]['content'] == html_doc_body_ok
    assert data['data'][0]['url'] == 'https://example.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert 'date_added' in data['data'][0]
    assert len(data['data'][0]['tags']) == 0


@patch('requests.get')
def test_add_article_no_category(get_mock, fake_request_ok, app, user_1):
    get_mock.return_value = fake_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/articles',
        data=json.dumps(dict(url='https://example.com', category_id=1)),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    check_500_category_not_found(response)


@patch('requests.get')
def test_add_article_invalid_payload(
    get_mock, fake_request_ok, app, user_1, cat_1
):
    get_mock.return_value = fake_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/articles',
        data=json.dumps(dict(category_id=1)),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    check_400_invalid_payload(response)


@patch('requests.get')
def test_add_article_invalid_content(
    get_mock, fake_request_ko, app, user_1, cat_1
):
    get_mock.return_value = fake_request_ko.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/articles',
        data=json.dumps(dict(url='https://example.com', category_id=1)),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    check_500_error(response)


@patch('requests.get')
def test_patch_article_add_comments_ok(
    get_mock, fake_request_ok, app, user_1, article_1
):
    get_mock.return_value = fake_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(comments='just a comment')),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 1
    assert data['data'][0]['title'] == 'Python tips'
    assert data['data'][0]['content'] == '<html></html>'
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] == 'just a comment'
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False


@patch('requests.get')
def test_patch_article_change_category_ok(
    get_mock, fake_request_ok, app, user_1, article_1, cat_4
):
    get_mock.return_value = fake_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(category_id=2)),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 1
    assert data['data'][0]['title'] == 'Python tips'
    assert data['data'][0]['content'] == '<html></html>'
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['category']['id'] == 2
    assert data['data'][0]['category']['name'] == 'moto'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False


@patch('requests.get')
def test_patch_article_invalid_payload(
    get_mock, fake_request_ok, app, user_1, article_1
):
    get_mock.return_value = fake_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict()),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    check_400_invalid_payload(response)


@patch('requests.get')
def test_patch_article_incorrect_category_ok(
    get_mock, fake_request_ok, app, user_1, article_1
):
    get_mock.return_value = fake_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(category_id=999)),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    check_500_category_not_found(response)


@patch('requests.get')
def test_patch_article_not_existing(
    get_mock, fake_request_ok, app, user_1, cat_1
):
    get_mock.return_value = fake_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(category_id=1)),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    check_404_article_not_found(response)


@patch('requests.get')
def test_patch_article_another_user_category(
    get_mock, fake_request_ok, app, user_1, article_1, cat_2
):
    get_mock.return_value = fake_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(category_id=2)),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    check_500_category_not_found(response)


@patch('requests.get')
def test_patch_article_another_user_article(
    get_mock, fake_request_ok, app, user_1, article_3
):
    get_mock.return_value = fake_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(category_id=2)),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    check_404_article_not_found(response)


def test_delete_article(app, user_1, article_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.delete(
        '/api/articles/1',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    assert response.status_code == 204


def test_delete_another_user_article(app, user_1, article_3):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.delete(
        '/api/articles/1',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    check_404_article_not_found(response)


def test_delete_not_existing_article(app, user_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.delete(
        '/api/articles/999',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    check_404_article_not_found(response)
