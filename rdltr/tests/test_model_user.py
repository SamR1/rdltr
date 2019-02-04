def test_user_model(app, user_1):
    assert '<User \'test\'>' == str(user_1)
    assert 1 == user_1.id
    assert 'test' == user_1.username
    assert 'test@test.com' == user_1.email
    assert '12345678' != user_1.password
    assert 0 == len(user_1.categories)

    serialized_user = user_1.serialize()
    assert 1 == serialized_user['id']
    assert 'test' == serialized_user['username']
    assert 'created_at' in serialized_user
    assert [] == serialized_user['categories']
