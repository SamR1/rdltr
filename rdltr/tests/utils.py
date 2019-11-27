import json
import random
import string


def check_400_invalid_payload(response):
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert data['message'] == 'Invalid payload.'


def check_400_invalid_credentials(response):
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert data['message'] == 'Invalid credentials.'


def check_500_error(response):
    assert response.content_type == 'application/json'
    assert response.status_code == 500
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert (
        'Error. Please try again or contact the administrator.'
        in data['message']
    )


def random_string(length=8):
    return ''.join(random.choice(string.ascii_letters) for x in range(length))
