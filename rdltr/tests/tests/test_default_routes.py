import json


def test_default_route(app):
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    # data = response.data.decode()
    # assert data == 'Hello World!'


def test_default_api_route(app):
    client = app.test_client()
    response = client.get('/api/ping')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert 'pong' in data['message']
    assert 'success' in data['status']
