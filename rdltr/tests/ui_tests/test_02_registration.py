from rdltr.tests.utils import URL, random_string, register, register_valid_user


def test_register_ok(selenium):
    user_infos = register_valid_user(selenium)
    nav = selenium.find_element_by_tag_name('nav').text
    assert "Register" not in nav
    assert "Log in" not in nav
    assert user_infos['username'] in nav


def test_register_invalid_email(selenium):
    user_name = random_string()
    user_infos = {
        'username': user_name,
        'email': user_name,
        'password': 'p@ssw0rd',
        'password_conf': 'p@ssw0rd',
    }
    register(selenium, user_infos)

    assert selenium.current_url == f"{URL}register"
    nav = selenium.find_element_by_tag_name('nav').text
    assert "Register" in nav
    assert "Log in" in nav


def test_register_password_confirmation_not_ok(selenium):
    user_name = random_string()
    user_infos = {
        'username': user_name,
        'email': f'{user_name}@example.com',
        'password': 'p@ssw0rd',
        'password_conf': 'password',
    }
    register(selenium, user_infos)

    assert selenium.current_url == f"{URL}register"
    nav = selenium.find_element_by_tag_name('nav').text
    assert "Register" in nav
    assert "Log in" in nav

    errors = selenium.find_element_by_class_name('alert-danger').text
    assert "Password and password confirmation don't match" in errors


def test_register_multiple_errors(selenium):
    user_name = random_string(2)
    user_infos = {
        'username': user_name,
        'email': f'{user_name}@example',
        'password': 'pass',
        'password_conf': 'pass',
    }
    register(selenium, user_infos)

    assert selenium.current_url == f"{URL}register"
    nav = selenium.find_element_by_tag_name('nav').text
    assert "Register" in nav
    assert "Log in" in nav

    errors = selenium.find_element_by_class_name('alert-danger').text
    assert "Username: 3 to 12 characters required" in errors
    assert "Valid email must be provided" in errors
    assert "Password: 8 characters required" in errors
