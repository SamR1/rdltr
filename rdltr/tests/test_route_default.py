def test_default_route(app):
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    # data = response.data.decode()
    # assert data == 'Hello World!'
