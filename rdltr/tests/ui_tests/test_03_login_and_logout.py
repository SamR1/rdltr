from rdltr.tests.utils import login, random_string, register


def test_logout_and_login_ok(selenium):
    user_name = random_string()
    user_infos = {
        'username': user_name,
        'email': f'{user_name}@example.com',
        'password': 'p@ssw0rd',
        'password_conf': 'p@ssw0rd',
    }
    register(selenium, user_infos)
    nav = selenium.find_element_by_tag_name('nav')
    nav_text = nav.text
    assert "Register" not in nav_text
    assert "Log in" not in nav_text
    assert "Logout" in nav_text

    menus = nav.find_elements_by_class_name('menu')
    menus[2].click()

    login(selenium, user_infos)
    nav = selenium.find_element_by_tag_name('nav')
    nav_text = nav.text
    assert user_name in nav_text
    assert "Settings" in nav_text
    assert "Logout" in nav_text


def test_login_not_existing_user(selenium):
    user_name = random_string()
    user_infos = {
        'username': user_name,
        'email': f'{user_name}@example.com',
        'password': 'p@ssw0rd',
        'password_conf': 'p@ssw0rd',
    }

    login(selenium, user_infos, True)
    nav = selenium.find_element_by_tag_name('nav')
    nav_text = nav.text
    assert "Register" in nav_text
    assert "Log in" in nav_text
    errors = selenium.find_element_by_class_name('alert-danger').text
    assert "Invalid credentials." in errors
