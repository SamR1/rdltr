import json
from unittest.mock import patch

from rdltr.tests.utils import check_400_invalid_payload, check_500_error
from rdltr.tests.utils_requests import html_doc_body_ok


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
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre</head><body><p>Test</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert 'date_added' in data['data'][0]
    assert data['data'][0]['tags'][0]['name'] == 'tips'


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

    assert data['data'][0]['title'] == 'Another article'
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre2</head><body><p>Test2</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] == 'just a comment'
    assert data['data'][0]['read']
    assert data['data'][0]['favorite']
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert 'date_added' in data['data'][0]
    assert data['data'][0]['tags'] == []

    assert data['data'][1]['title'] == 'Python tips'
    assert (
        data['data'][1]['html_content']
        == '<html><head><title>Titre</head><body><p>Test</p></body></html>'
    )
    assert data['data'][1]['url'] == 'https://test.com'
    assert data['data'][1]['comments'] is None
    assert data['data'][1]['read'] is False
    assert data['data'][1]['favorite'] is False
    assert data['data'][1]['category']['id'] == 1
    assert data['data'][1]['category']['name'] == 'python'
    assert data['data'][1]['category']['description'] is None
    assert data['data'][1]['category']['is_default'] is False
    assert 'date_added' in data['data'][1]
    assert data['data'][1]['tags'][0]['name'] == 'tips'


def test_get_articles_pagination(app, articles_20):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.get(
        '/api/articles?page=1',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 12

    assert data['data'][0]['title'] == 'Python article 20'
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre20</head><body><p>Test20</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://python.com'
    assert data['data'][0]['category']['id'] == 1

    assert data['data'][11]['title'] == 'Python article 9'
    assert (
        data['data'][11]['html_content']
        == '<html><head><title>Titre9</head><body><p>Test9</p></body></html>'
    )
    assert data['data'][11]['url'] == 'https://python.com'
    assert data['data'][11]['category']['id'] == 1

    response = client.get(
        '/api/articles?page=2',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 8

    assert data['data'][0]['title'] == 'Python article 8'
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre8</head><body><p>Test8</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://python.com'
    assert data['data'][0]['category']['id'] == 1

    assert data['data'][7]['title'] == 'Python article 1'
    assert (
        data['data'][7]['html_content']
        == '<html><head><title>Titre1</head><body><p>Test1</p></body></html>'
    )
    assert data['data'][7]['url'] == 'https://python.com'
    assert data['data'][7]['category']['id'] == 1

    response = client.get(
        '/api/articles?page=3',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 0


def test_get_articles_filter_by_category(
    app, article_1, article_2, article_3, article_4
):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.get(
        '/api/articles?cat_id=3',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 1

    assert data['data'][0]['id'] == 4
    assert data['data'][0]['title'] == 'Great article'
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre4</head><body><p>Test4</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] == 'just a comment'
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 3

    response = client.get(
        '/api/articles?cat_id=4',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 0


def test_get_articles_filter_by_tag(
    app, article_1, article_2, article_3, article_4
):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.get(
        '/api/articles?tag_id=1',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 1

    assert data['data'][0]['id'] == 1
    assert data['data'][0]['title'] == 'Python tips'
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre</head><body><p>Test</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 1

    response = client.get(
        '/api/articles?tag_id=3',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 0


def test_get_articles_filter_by_query(
    app, article_1, article_2, article_3, article_4
):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.get(
        '/api/articles?q=Great article',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 1

    assert data['data'][0]['id'] == 4
    assert data['data'][0]['title'] == 'Great article'
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre4</head><body><p>Test4</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] == 'just a comment'
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 3

    response = client.get(
        '/api/articles?q=azerty',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 0


def test_get_articles_filter_by_read_status(
    app, article_1, article_2, article_3, article_4
):
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
    assert len(data['data']) == 3

    response = client.get(
        '/api/articles?not_read=true',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 2

    assert data['data'][0]['title'] == 'Great article'
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre4</head><body><p>Test4</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] == 'just a comment'
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 3
    assert data['data'][0]['category']['name'] == 'moto'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert 'date_added' in data['data'][0]
    assert data['data'][0]['tags'] == []

    assert data['data'][1]['title'] == 'Python tips'
    assert (
        data['data'][1]['html_content']
        == '<html><head><title>Titre</head><body><p>Test</p></body></html>'
    )
    assert data['data'][1]['url'] == 'https://test.com'
    assert data['data'][1]['comments'] is None
    assert data['data'][1]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][1]['category']['id'] == 1
    assert data['data'][1]['category']['name'] == 'python'
    assert data['data'][1]['category']['description'] is None
    assert data['data'][1]['category']['is_default'] is False
    assert 'date_added' in data['data'][1]
    assert data['data'][1]['tags'][0]['name'] == 'tips'


def test_get_articles_filter_by_favorites(
    app, article_1, article_2, article_3, article_4
):
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
    assert len(data['data']) == 3

    response = client.get(
        '/api/articles?only_favorites=true',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 1

    assert data['data'][0]['title'] == 'Another article'
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre2</head><body><p>Test2</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] == 'just a comment'
    assert data['data'][0]['read']
    assert data['data'][0]['favorite']
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert 'date_added' in data['data'][0]
    assert data['data'][0]['tags'] == []


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
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre</head><body><p>Test</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert 'date_added' in data['data'][0]
    assert data['data'][0]['tags'][0]['name'] == 'tips'


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
    get_mock, mock_request_ok, app, user_1, cat_3
):
    get_mock.return_value = mock_request_ok.return_value
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
    assert data['data'][0]['html_content'] == html_doc_body_ok
    assert data['data'][0]['url'] == 'https://example.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default']
    assert 'date_added' in data['data'][0]
    assert len(data['data'][0]['tags']) == 0


@patch('requests.get')
def test_add_article_to_category_no_tags(
    get_mock, mock_request_ok, app, user_1, cat_1
):
    get_mock.return_value = mock_request_ok.return_value
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
    assert data['data'][0]['html_content'] == html_doc_body_ok
    assert data['data'][0]['url'] == 'https://example.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert 'date_added' in data['data'][0]
    assert len(data['data'][0]['tags']) == 0


@patch('requests.get')
def test_add_article_to_category_with_no_existing_tags(
    get_mock, mock_request_ok, app, user_1, cat_1
):
    get_mock.return_value = mock_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/articles',
        data=json.dumps(
            dict(
                url='https://example.com', category_id=1, tags=['tuto', 'css']
            )
        ),
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
    assert data['data'][0]['html_content'] == html_doc_body_ok
    assert data['data'][0]['url'] == 'https://example.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert 'date_added' in data['data'][0]
    assert len(data['data'][0]['tags']) == 2
    assert data['data'][0]['tags'][0]['name'] in ['css', 'tuto']
    assert data['data'][0]['tags'][1]['name'] in ['css', 'tuto']


@patch('requests.get')
def test_add_article_to_category_with_existing_tag(
    get_mock, mock_request_ok, app, user_1, cat_1, tag_1
):
    get_mock.return_value = mock_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/articles',
        data=json.dumps(
            dict(
                url='https://example.com', category_id=1, tags=['tips', 'css']
            )
        ),
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
    assert data['data'][0]['html_content'] == html_doc_body_ok
    assert data['data'][0]['url'] == 'https://example.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert 'date_added' in data['data'][0]
    assert len(data['data'][0]['tags']) == 2
    assert data['data'][0]['tags'][0]['name'] == 'tips'
    assert data['data'][0]['tags'][1]['name'] == 'css'


@patch('requests.get')
def test_add_article_no_category(get_mock, mock_request_ok, app, user_1):
    get_mock.return_value = mock_request_ok.return_value
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
    get_mock, mock_request_ok, app, user_1, cat_1
):
    get_mock.return_value = mock_request_ok.return_value
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
    get_mock, mock_request_empty, app, user_1, cat_1
):
    get_mock.return_value = mock_request_empty.return_value
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
    assert response.content_type == 'application/json'
    assert response.status_code == 500
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert 'Error. Cannot parse the document.' in data['message']


@patch('requests.get')
def test_add_article_not_found(
    get_mock, mock_request_not_found, app, user_1, cat_1
):
    get_mock.return_value = mock_request_not_found.return_value
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
    assert response.content_type == 'application/json'
    assert response.status_code == 500
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert (
        'Error. Cannot get the requested resource, '
        'please check the URL (code: 404)' in data['message']
    )


def test_add_article_invalid_url(app, user_1, cat_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/articles',
        data=json.dumps(dict(url='invalid-url', category_id=1)),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert data['message'] == 'Error: Invalid URL, please check it.'


def test_add_article_no_existing_url(app, user_1, cat_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/articles',
        data=json.dumps(
            dict(url='http://not-existing-url.not', category_id=1)
        ),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    assert response.status_code == 500
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert (
        data['message'] == 'Error. Cannot connect to the URL, please check it.'
    )


@patch('requests.get')
def test_patch_article_add_comments_ok(
    get_mock, mock_request_ok, app, user_1, article_1
):
    get_mock.return_value = mock_request_ok.return_value
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
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre</head><body><p>Test</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] == 'just a comment'
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert len(data['data'][0]['tags']) == 2
    assert data['data'][0]['tags'][0]['name'] == 'tips'
    assert data['data'][0]['tags'][1]['name'] == 'tuto'


@patch('requests.get')
def test_patch_article_change_category_ok(
    get_mock, mock_request_ok, app, user_1, article_1, cat_4
):
    get_mock.return_value = mock_request_ok.return_value
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
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre</head><body><p>Test</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 2
    assert data['data'][0]['category']['name'] == 'moto'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert len(data['data'][0]['tags']) == 2
    assert data['data'][0]['tags'][0]['name'] == 'tips'
    assert data['data'][0]['tags'][1]['name'] == 'tuto'


@patch('requests.get')
def test_patch_article_change_with_new_tags(
    get_mock, mock_request_ok, app, user_1, article_1, cat_4
):
    get_mock.return_value = mock_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(category_id=2, tags=['new'])),
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
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre</head><body><p>Test</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 2
    assert data['data'][0]['category']['name'] == 'moto'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert len(data['data'][0]['tags']) == 1
    assert data['data'][0]['tags'][0]['name'] == 'new'


@patch('requests.get')
def test_patch_article_change_with_existing_tag(
    get_mock, mock_request_ok, app, user_1, article_1, cat_4, tag_1
):
    get_mock.return_value = mock_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(category_id=2, tags=['tips'])),
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
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre</head><body><p>Test</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 2
    assert data['data'][0]['category']['name'] == 'moto'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert len(data['data'][0]['tags']) == 1
    assert data['data'][0]['tags'][0]['id'] == 1
    assert data['data'][0]['tags'][0]['name'] == 'tips'


@patch('requests.get')
def test_patch_article_change_replacing_tag(
    get_mock, mock_request_ok, app, user_1, article_1, cat_4, tag_1
):
    get_mock.return_value = mock_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(category_id=2, tags=['tips', 'new'])),
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
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre</head><body><p>Test</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 2
    assert data['data'][0]['category']['name'] == 'moto'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert len(data['data'][0]['tags']) == 2
    assert data['data'][0]['tags'][0]['name'] == 'tips'
    assert data['data'][0]['tags'][1]['name'] == 'new'


@patch('requests.get')
def test_patch_article_remove_tags(
    get_mock, mock_request_ok, app, user_1, article_1
):
    get_mock.return_value = mock_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(tags=[])),
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
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre</head><body><p>Test</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert len(data['data'][0]['tags']) == 0


@patch('requests.get')
def test_patch_article_tags_error(
    get_mock, mock_request_ok, app, user_1, article_1
):
    get_mock.return_value = mock_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(tags=[[]])),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    check_500_error(response)


@patch('requests.get')
def test_patch_article_change_read_status_ok(
    get_mock, mock_request_ok, app, article_1
):
    get_mock.return_value = mock_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(update_read_status=True)),
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
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre</head><body><p>Test</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is True
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert len(data['data'][0]['tags']) == 2
    assert data['data'][0]['tags'][0]['name'] == 'tips'
    assert data['data'][0]['tags'][1]['name'] == 'tuto'

    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(update_read_status=False)),
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
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre</head><body><p>Test</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert len(data['data'][0]['tags']) == 2
    assert data['data'][0]['tags'][0]['name'] == 'tips'
    assert data['data'][0]['tags'][1]['name'] == 'tuto'

    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(update_read_status="")),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    check_500_error(response)


@patch('requests.get')
def test_patch_article_change_favorite_status_ok(
    get_mock, mock_request_ok, app, article_1
):
    get_mock.return_value = mock_request_ok.return_value
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(update_favorite=True)),
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
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre</head><body><p>Test</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is True
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert len(data['data'][0]['tags']) == 2
    assert data['data'][0]['tags'][0]['name'] == 'tips'
    assert data['data'][0]['tags'][1]['name'] == 'tuto'

    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(update_favorite=False)),
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
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre</head><body><p>Test</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert len(data['data'][0]['tags']) == 2
    assert data['data'][0]['tags'][0]['name'] == 'tips'
    assert data['data'][0]['tags'][1]['name'] == 'tuto'

    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(update_favorite="")),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    check_500_error(response)


@patch('requests.get')
def test_patch_article_reload_content(
    get_mock, mock_request_ok, app, article_1
):
    get_mock.return_value = mock_request_ok.return_value
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
        content_type='application/json',
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 1
    assert data['data'][0]['title'] == 'Python tips'
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre</head><body><p>Test</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert len(data['data'][0]['tags']) == 2
    assert data['data'][0]['tags'][0]['name'] == 'tips'
    assert data['data'][0]['tags'][1]['name'] == 'tuto'

    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(reload=True)),
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
    assert data['data'][0]['title'] == 'this is a title'
    assert (
        data['data'][0]['html_content']
        == '<body id="readabilityBody">\n        <p>this is a paragraph</p>\n    </body>\n'  # noqa
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert len(data['data'][0]['tags']) == 2
    assert data['data'][0]['tags'][0]['name'] == 'tips'
    assert data['data'][0]['tags'][1]['name'] == 'tuto'


@patch('requests.get')
def test_patch_article_reload_content_false(
    get_mock, mock_request_ok, app, article_1
):
    get_mock.return_value = mock_request_ok.return_value
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
        content_type='application/json',
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert len(data['data']) == 1
    assert data['data'][0]['title'] == 'Python tips'
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre</head><body><p>Test</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert len(data['data'][0]['tags']) == 2
    assert data['data'][0]['tags'][0]['name'] == 'tips'
    assert data['data'][0]['tags'][1]['name'] == 'tuto'

    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(reload=False)),
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
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre</head><body><p>Test</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert len(data['data'][0]['tags']) == 2
    assert data['data'][0]['tags'][0]['name'] == 'tips'
    assert data['data'][0]['tags'][1]['name'] == 'tuto'

    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(reload="")),
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
    assert (
        data['data'][0]['html_content']
        == '<html><head><title>Titre</head><body><p>Test</p></body></html>'
    )
    assert data['data'][0]['url'] == 'https://test.com'
    assert data['data'][0]['comments'] is None
    assert data['data'][0]['read'] is False
    assert data['data'][0]['favorite'] is False
    assert data['data'][0]['category']['id'] == 1
    assert data['data'][0]['category']['name'] == 'python'
    assert data['data'][0]['category']['description'] is None
    assert data['data'][0]['category']['is_default'] is False
    assert len(data['data'][0]['tags']) == 2
    assert data['data'][0]['tags'][0]['name'] == 'tips'
    assert data['data'][0]['tags'][1]['name'] == 'tuto'


def test_patch_article_reload_url_ko(app, article_1):
    article_1.url = 'http://not-existing-url.not'
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.patch(
        '/api/articles/1',
        data=json.dumps(dict(reload=True)),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    assert response.status_code == 500
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert (
        data['message'] == 'Error. Cannot connect to the URL, please check it.'
    )


@patch('requests.get')
def test_patch_article_invalid_payload(
    get_mock, mock_request_ok, app, user_1, article_1
):
    get_mock.return_value = mock_request_ok.return_value
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
    get_mock, mock_request_ok, app, user_1, article_1
):
    get_mock.return_value = mock_request_ok.return_value
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
    get_mock, mock_request_ok, app, user_1, cat_1
):
    get_mock.return_value = mock_request_ok.return_value
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
    get_mock, mock_request_ok, app, user_1, article_1, cat_2
):
    get_mock.return_value = mock_request_ok.return_value
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
    get_mock, mock_request_ok, app, user_1, article_3
):
    get_mock.return_value = mock_request_ok.return_value
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
