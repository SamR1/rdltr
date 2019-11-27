from rdltr.tests.utils import URL, random_string


def register(selenium, user_infos):
    selenium.get(f"{URL}register")
    nav = selenium.find_element_by_tag_name('nav')
    menus = nav.find_elements_by_class_name('menu')
    assert "Register" in menus[0].text
    menus[0].click()
    selenium.implicitly_wait(2)

    username = selenium.find_element_by_id('username')
    username.send_keys(user_infos.get('username'))
    email = selenium.find_element_by_id('email')
    email.send_keys(user_infos.get('email'))
    password = selenium.find_element_by_id('password')
    password.send_keys(user_infos.get('password'))
    password_conf = selenium.find_element_by_id('confirm-password')
    password_conf.send_keys(user_infos.get('password_conf'))

    submit_button = selenium.find_element_by_tag_name('button')
    submit_button.click()


def test_register_ok(selenium):
    user_name = random_string()
    user_infos = {
        'username': user_name,
        'email': f'{user_name}@example.com',
        'password': 'p@ssw0rd',
        'password_conf': 'p@ssw0rd',
    }
    register(selenium, user_infos)
    nav = selenium.find_element_by_tag_name('nav').text
    assert "Register" not in nav
    assert "Log in" not in nav
    assert user_name in nav


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
