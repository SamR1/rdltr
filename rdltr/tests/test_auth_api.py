import json
import time


def test_user_registration(app):
    client = app.test_client()
    response = client.post(
        '/api/auth/register',
        data=json.dumps(
            dict(
                username='justatest',
                email='test@test.com',
                password='12345678',
                password_conf='12345678',
            )
        ),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert data['message'] == 'Successfully registered.'
    assert data['auth_token']
    assert response.content_type == 'application/json'
    assert response.status_code == 201


def test_user_registration_user_already_exists(app, user_1):
    client = app.test_client()
    response = client.post(
        '/api/auth/register',
        data=json.dumps(
            dict(
                username='test',
                email='test@test.com',
                password='12345678',
                password_conf='12345678',
            )
        ),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert data['message'] == 'Sorry. That user already exists.'
    assert response.content_type == 'application/json'
    assert response.status_code == 400


def test_user_registration_invalid_short_username(app):
    client = app.test_client()
    response = client.post(
        '/api/auth/register',
        data=json.dumps(
            dict(
                username='t',
                email='test@test.com',
                password='12345678',
                password_conf='12345678',
            )
        ),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert (
        data['message'] == "Errors: Username: 3 to 12 characters required.\n"
    )
    assert response.content_type == 'application/json'
    assert response.status_code == 400


def test_user_registration_invalid_long_username(app):
    client = app.test_client()
    response = client.post(
        '/api/auth/register',
        data=json.dumps(
            dict(
                username='testestestestestest',
                email='test@test.com',
                password='12345678',
                password_conf='12345678',
            )
        ),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert (
        data['message'] == "Errors: Username: 3 to 12 characters required.\n"
    )
    assert response.content_type == 'application/json'
    assert response.status_code == 400


def test_user_registration_invalid_email(app):
    client = app.test_client()
    response = client.post(
        '/api/auth/register',
        data=json.dumps(
            dict(
                username='test',
                email='test@test',
                password='12345678',
                password_conf='12345678',
            )
        ),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert data['message'] == "Errors: Valid email must be provided.\n"
    assert response.content_type == 'application/json'
    assert response.status_code == 400


def test_user_registration_invalid_short_password(app):
    client = app.test_client()
    response = client.post(
        '/api/auth/register',
        data=json.dumps(
            dict(
                username='test',
                email='test@test.com',
                password='1234567',
                password_conf='1234567',
            )
        ),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert data['message'] == "Errors: Password: 8 characters required.\n"
    assert response.content_type == 'application/json'
    assert response.status_code == 400


def test_user_registration_mismatched_password(app):
    client = app.test_client()
    response = client.post(
        '/api/auth/register',
        data=json.dumps(
            dict(
                username='test',
                email='test@test.com',
                password='12345678',
                password_conf='87654321',
            )
        ),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert (
        data['message']
        == "Errors: Password and password confirmation don\'t match.\n"
    )
    assert response.content_type == 'application/json'
    assert response.status_code == 400


def test_user_registration_invalid_json(app):
    client = app.test_client()
    response = client.post(
        '/api/auth/register',
        data=json.dumps(dict()),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert response.status_code, 400
    assert 'Invalid payload.', data['message']
    assert 'error', data['status']


def test_user_registration_invalid_json_keys_no_username(app):
    client = app.test_client()
    response = client.post(
        '/api/auth/register',
        data=json.dumps(
            dict(
                email='test@test.com',
                password='12345678',
                password_conf='12345678',
            )
        ),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'Invalid payload.' in data['message']
    assert 'error' in data['status']


def test_user_registration_invalid_json_keys_no_email(app):
    client = app.test_client()
    response = client.post(
        '/api/auth/register',
        data=json.dumps(
            dict(
                username='test', password='12345678', password_conf='12345678'
            )
        ),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'Invalid payload.' in data['message']
    assert 'error' in data['status']


def test_user_registration_invalid_json_keys_no_password(app):
    client = app.test_client()
    response = client.post(
        '/api/auth/register',
        data=json.dumps(
            dict(
                username='test',
                email='test@test.com',
                password_conf='12345678',
            )
        ),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'Invalid payload.', data['message']
    assert 'error', data['status']


def test_user_registration_invalid_json_keys_no_password_conf(app):
    client = app.test_client()
    response = client.post(
        '/api/auth/register',
        data=json.dumps(
            dict(username='test', email='test@test.com', password='12345678')
        ),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'Invalid payload.' in data['message']
    assert 'error' in data['status']


def test_user_registration_invalid_data(app):
    client = app.test_client()
    response = client.post(
        '/api/auth/register',
        data=json.dumps(
            dict(
                username=1,
                email='test@test.com',
                password='12345678',
                password_conf='12345678',
            )
        ),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 500
    assert (
        'Error. Please try again or contact the administrator.'
        in data['message']
    )
    assert 'error' in data['status']


def test_user_registration_no_db(app_wo_db):
    client = app_wo_db.test_client()
    response = client.post(
        '/api/auth/register',
        data=json.dumps(
            dict(
                username='test',
                email='test@test.com',
                password='12345678',
                password_conf='12345678',
            )
        ),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 500
    assert (
        'Error. Please try again or contact the administrator.'
        in data['message']
    )
    assert 'error' in data['status']


def test_login_registered_user(app, user_1):
    client = app.test_client()
    response = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert data['message'] == 'Successfully logged in.'
    assert data['auth_token']
    assert response.content_type == 'application/json'
    assert response.status_code == 200


def test_login_no_registered_user(app):
    client = app.test_client()
    response = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert data['message'] == 'Invalid credentials.'
    assert response.content_type == 'application/json'
    assert response.status_code == 404


def test_login_invalid_payload(app):
    client = app.test_client()
    response = client.post(
        '/api/auth/login',
        data=json.dumps(dict()),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert data['message'] == 'Invalid payload.'
    assert response.content_type == 'application/json'
    assert response.status_code == 400


def test_login_registered_user_invalid_password(app, user_1):
    client = app.test_client()
    response = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='123456789')),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert data['message'] == 'Invalid credentials.'
    assert response.content_type == 'application/json'
    assert response.status_code == 404


def test_login_no_db(app_wo_db):
    client = app_wo_db.test_client()
    response = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='123456789')),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 500
    assert (
        'Error. Please try again or contact the administrator.'
        in data['message']
    )
    assert 'error' in data['status']


def test_logout(app, user_1):
    client = app.test_client()
    # user login
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    # valid token logout
    response = client.get(
        '/api/auth/logout',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert data['message'] == 'Successfully logged out.'
    assert response.status_code == 200


def test_logout_expired_token(app, user_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    # invalid token logout
    time.sleep(4)
    response = client.get(
        '/api/auth/logout',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert data['message'] == 'Signature expired. Please log in again.'
    assert response.status_code == 401


def test_logout_invalid_token(app):
    client = app.test_client()
    response = client.get(
        '/api/auth/logout', headers=dict(Authorization='Bearer invalid')
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert data['message'] == 'Invalid token. Please log in again.'
    assert response.status_code == 401


def test_logout_invalid_headers(app):
    client = app.test_client()
    response = client.get('/api/auth/logout', headers=dict())
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert data['message'] == 'Provide a valid auth token.'
    assert response.status_code == 401


def test_logout_invalid_user(app, user_1):
    client = app.test_client()
    # user login
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )

    # change user id
    user_1.id = 10

    response = client.get(
        '/api/auth/logout',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert data['message'] == 'Something went wrong. Please contact us.'
    assert response.status_code == 401
