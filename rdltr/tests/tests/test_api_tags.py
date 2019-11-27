import json

from rdltr.tests.utils import check_400_invalid_payload


def check_404_tag(response):
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data['status'] == 'not found'
    assert data['message'] == 'Tag no found.'


def test_get_no_tags(app, user_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.get(
        '/api/tags',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert data['data'] == []


def test_get_one_tag(app, user_1, tag_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.get(
        '/api/tags',
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
    assert data['data'][0]['user_id'] == 1
    assert data['data'][0]['name'] == 'tips'


def test_add_tag(app, user_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/tags',
        data=json.dumps(dict(name='moto')),
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
    assert data['data'][0]['id'] == 1
    assert data['data'][0]['user_id'] == 1
    assert data['data'][0]['name'] == 'moto'

    response = client.get(
        '/api/auth/profile',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['user'] is not None
    assert data['user']['username'] == 'test'
    assert data['user']['email'] == 'test@test.com'
    assert data['user']['created_at']
    assert data['user']['categories'] == []
    assert data['user']['tags'][0]['id'] == 1
    assert data['user']['tags'][0]['user_id'] == 1
    assert data['user']['tags'][0]['name'] == 'moto'


def test_add_tag_invalid_payload(app, user_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/tags',
        data=json.dumps(dict(color='blue')),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    check_400_invalid_payload(response)


def test_add_existing_tag(app, user_1, tag_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/tags',
        data=json.dumps(dict(name='tips')),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert data['message'] == 'A tag named "tips" already exists.'


def test_add_another_user_existing_tag(app, user_1, tag_3):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/tags',
        data=json.dumps(dict(name='moto')),
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
    assert data['data'][0]['id'] == 2
    assert data['data'][0]['user_id'] == 1
    assert data['data'][0]['name'] == 'moto'


def test_update_existing(app, user_1, tag_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.patch(
        '/api/tags/1',
        data=json.dumps(dict(name='new label')),
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
    assert data['data'][0]['id'] == 1
    assert data['data'][0]['user_id'] == 1
    assert data['data'][0]['name'] == 'new label'


def test_update_another_user_tag(app, user_1, tag_3):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.patch(
        '/api/tags/3',
        data=json.dumps(dict(name='new label', description='new description')),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    check_404_tag(response)


def test_update_not_existing_tag(app, user_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.patch(
        '/api/tags/100',
        data=json.dumps(dict(name='new label', color='blue')),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data['status'] == 'not found'
    assert data['message'] == 'Tag no found.'


def test_update_tag_invalid_payload(app, user_1, tag_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.patch(
        '/api/tags/1',
        data=json.dumps(dict()),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    check_400_invalid_payload(response)


def test_delete_tag(app, user_1, tag_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.delete(
        '/api/tags/1',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    assert response.status_code == 204


def test_delete_another_user_tag(app, user_1, tag_3):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.delete(
        '/api/tags/1',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    check_404_tag(response)


def test_delete_not_existing_tag(app, user_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.delete(
        '/api/tags/999',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
        content_type='application/json',
    )
    check_404_tag(response)
