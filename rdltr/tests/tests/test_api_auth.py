import json
import time

from rdltr.tests.utils import (
    check_400_invalid_credentials,
    check_400_invalid_payload,
    check_500_error,
)


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
    check_400_invalid_payload(response)


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
    check_400_invalid_payload(response)


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
    check_400_invalid_payload(response)


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
    check_400_invalid_payload(response)


def test_user_registration_invalid_json_keys_no_password_conf(app):
    client = app.test_client()
    response = client.post(
        '/api/auth/register',
        data=json.dumps(
            dict(username='test', email='test@test.com', password='12345678')
        ),
        content_type='application/json',
    )
    check_400_invalid_payload(response)


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
    check_500_error(response)


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
    check_500_error(response)


def test_user_registration_not_allowed(app_no_registration):
    client = app_no_registration.test_client()
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

    assert response.content_type == 'application/json'
    assert response.status_code == 403
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert data['message'] == 'Error. Registration is disabled.'


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
    check_400_invalid_credentials(response)


def test_login_invalid_payload(app):
    client = app.test_client()
    response = client.post(
        '/api/auth/login',
        data=json.dumps(dict()),
        content_type='application/json',
    )
    check_400_invalid_payload(response)


def test_login_registered_user_invalid_password(app, user_1):
    client = app.test_client()
    response = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='123456789')),
        content_type='application/json',
    )
    check_400_invalid_credentials(response)


def test_login_no_db(app_wo_db):
    client = app_wo_db.test_client()
    response = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='123456789')),
        content_type='application/json',
    )
    check_500_error(response)


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


def test_user_profile_ok(app, user_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
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
    assert data['user']['tags'] == []


def test_user_profile_full_ok(app):
    client = app.test_client()
    resp_register = client.post(
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
    response = client.get(
        '/api/auth/profile',
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_register.data.decode())['auth_token']
        ),
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['user'] is not None
    assert data['user']['username'] == 'justatest'
    assert data['user']['email'] == 'test@test.com'
    assert data['user']['created_at']
    assert data['user']['categories'] == [
        {
            'id': 1,
            'user_id': 1,
            'name': 'default',
            'description': 'Default category',
            'is_default': True,
        }
    ]
    assert data['user']['tags'] == []


def test_user_profile_invalid_token(app, user_1):
    client = app.test_client()
    response = client.get(
        '/api/auth/profile', headers=dict(Authorization='Bearer xxx')
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 401
    assert data['status'] == 'error'
    assert data['message'] == 'Invalid token. Please log in again.'


def test_user_profile_no_token(app, user_1):
    client = app.test_client()
    response = client.get('/api/auth/profile')
    data = json.loads(response.data.decode())

    assert response.status_code == 401
    assert data['status'] == 'error'
    assert data['message'] == 'Provide a valid auth token.'


def test_update_password_ok(app, user_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/auth/profile/edit',
        content_type='application/json',
        data=json.dumps(
            dict(
                old_password='12345678',
                new_password='abcdefgh',
                new_password_conf='abcdefgh',
            )
        ),
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


def test_update_password_invalid_payload(app, user_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/auth/profile/edit',
        content_type='application/json',
        data=json.dumps(
            dict(new_password='abcdefgh', new_password_conf='abcdefgh')
        ),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    check_400_invalid_payload(response)


def test_update_password_no_payload(app, user_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/auth/profile/edit',
        content_type='application/json',
        data=json.dumps(dict()),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    check_400_invalid_payload(response)


def test_update_password_incorrect_password(app, user_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/auth/profile/edit',
        content_type='application/json',
        data=json.dumps(
            dict(
                old_password='00000000',
                new_password='abcdefgh',
                new_password_conf='abcdefgh',
            )
        ),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    check_400_invalid_credentials(response)


def test_update_password_invalid_new_password(app, user_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/auth/profile/edit',
        content_type='application/json',
        data=json.dumps(
            dict(
                old_password='12345678',
                new_password='abcdef',
                new_password_conf='abcdef',
            )
        ),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert data['status'] == 'error'
    assert data['message'] == 'Errors: Password: 8 characters required.\n'


def test_update_password_diff_password(app, user_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/auth/profile/edit',
        content_type='application/json',
        data=json.dumps(
            dict(
                old_password='12345678',
                new_password='abcdefgh',
                new_password_conf='abcdefghi',
            )
        ),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert data['status'] == 'error'
    assert data['message'] == (
        'Errors: Password and password confirmation don\'t match.\n'
    )


def test_update_password_invalid_password_type(app, user_1):
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    response = client.post(
        '/api/auth/profile/edit',
        content_type='application/json',
        data=json.dumps(
            dict(
                old_password='12345678',
                new_password=12_345_678,
                new_password_conf=12_345_678,
            )
        ),
        headers=dict(
            Authorization='Bearer '
            + json.loads(resp_login.data.decode())['auth_token']
        ),
    )
    check_500_error(response)
