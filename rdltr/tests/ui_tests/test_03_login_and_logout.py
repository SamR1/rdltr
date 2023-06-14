from rdltr.tests.utils import (
    login,
    login_valid_user,
    random_string,
    register_valid_user,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


def test_logout_and_login_ok(selenium: WebDriver) -> None:
    user_infos = register_valid_user(selenium)
    nav = selenium.find_element(By.TAG_NAME, 'nav')
    nav_text = nav.text
    assert 'Register' not in nav_text
    assert 'Log in' not in nav_text
    assert 'Logout' in nav_text

    menus = nav.find_elements(By.CLASS_NAME, 'menu')
    menus[2].click()

    login_valid_user(selenium, user_infos)
    nav = selenium.find_element(By.TAG_NAME, 'nav')
    nav_text = nav.text
    assert user_infos['username'] in nav_text
    assert 'Settings' in nav_text
    assert 'Logout' in nav_text


def test_login_not_existing_user(selenium: WebDriver) -> None:
    user_name = random_string()
    user_infos = {
        'username': user_name,
        'email': f'{user_name}@example.com',
        'password': 'p@ssw0rd',
        'password_conf': 'p@ssw0rd',
    }

    login(selenium, user_infos, True)
    nav = selenium.find_element(By.TAG_NAME, 'nav')
    nav_text = nav.text
    assert 'Register' in nav_text
    assert 'Log in' in nav_text
    errors = selenium.find_element(By.CLASS_NAME, 'alert-danger').text
    assert 'Invalid credentials.' in errors


def test_password_update_ok(selenium: WebDriver) -> None:
    user_infos = register_valid_user(selenium)
    menus = selenium.find_elements(By.CLASS_NAME, 'menu')
    menus[2].click()
    login_valid_user(selenium, user_infos)

    # click on user name
    menus = selenium.find_elements(By.CLASS_NAME, 'menu')
    menus[0].click()

    # click on 'Change password'
    submit_button = selenium.find_element(By.TAG_NAME, 'button')
    submit_button.click()

    # update password
    new_password = 'newp@ssw0rd'
    password = selenium.find_element(By.ID, 'oldPassword')
    password.send_keys(user_infos.get('password'))

    password = selenium.find_element(By.ID, 'password')
    password.send_keys(new_password)
    password_conf = selenium.find_element(By.ID, 'confirm-password')
    password_conf.send_keys(new_password)

    submit_button = selenium.find_element(By.TAG_NAME, 'button')
    submit_button.click()

    # log out
    menus = selenium.find_elements(By.CLASS_NAME, 'menu')
    menus[2].click()

    # log in
    user_infos['password'] = user_infos['password_conf'] = new_password
    login_valid_user(selenium, user_infos)
