from rdltr.tests.utils import login, random_string, register_valid_user


def test_logout_and_login_ok(selenium):
    user_infos = register_valid_user(selenium)
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
    assert user_infos['username'] in nav_text
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


def test_password_update_ok(selenium):
    user_infos = register_valid_user(selenium)
    menus = selenium.find_elements_by_class_name('menu')
    menus[2].click()
    login(selenium, user_infos)
    menus = selenium.find_elements_by_class_name('menu')
    menus[0].click()

    submit_button = selenium.find_element_by_tag_name('button')
    submit_button.click()

    new_password = 'newp@ssw0rd'
    password = selenium.find_element_by_id('oldPassword')
    password.send_keys(user_infos.get('password'))

    password = selenium.find_element_by_id('password')
    password.send_keys(new_password)
    password_conf = selenium.find_element_by_id('confirm-password')
    password_conf.send_keys(new_password)

    submit_button = selenium.find_element_by_tag_name('button')
    submit_button.click()

    menus = selenium.find_elements_by_class_name('menu')
    menus[2].click()

    user_infos['password'] = new_password
    login(selenium, user_infos)
