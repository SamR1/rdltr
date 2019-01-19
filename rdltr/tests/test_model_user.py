def test_user_model(app, user_1):
    assert '<User \'test\'>' == str(user_1)
    assert 1 == user_1.id
    assert 'test' == user_1.username
    assert 'test@test.com' == user_1.email
    assert '12345678' != user_1.password
    assert user_1.check_password('12345678') is True
    assert user_1.check_password('12345679') is False
