import json

from flask import Flask


def test_default_route(app: Flask) -> None:
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert '<title>rdltr</title>' in response.data.decode()


def test_default_api_route(app: Flask) -> None:
    client = app.test_client()
    response = client.get('/api/ping')
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert 'pong' in data['message']
    assert 'success' in data['status']
