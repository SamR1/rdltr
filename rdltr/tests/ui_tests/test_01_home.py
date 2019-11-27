import os

from rdltr.tests.utils import random_string

URL = (
    f"http://{os.getenv('RDLTR_HOST', '0.0.0.0')}:"
    f"{os.getenv('RDLTR_PORT', '5000')}/"
)


def test_index_ok(selenium):
    selenium.get(URL)

    header = selenium.find_element_by_tag_name('header')
    logo = header.find_element_by_class_name('logo').text
    assert "rdltr a simple \"read-it later\"" in logo

    nav = header.find_element_by_tag_name('nav').text
    assert "Register" in nav
    assert "Log in" in nav

    connexion_form = selenium.find_element_by_id('actionType').text
    assert "Email" in connexion_form
    assert "Password" in connexion_form


def test_register_ok(selenium):
    selenium.get(f"{URL}register")

    nav = selenium.find_element_by_tag_name('nav')
    menus = nav.find_elements_by_class_name('menu')
    assert "Register" in menus[0].text
    menus[0].click()

    user_name = random_string()

    username = selenium.find_element_by_id('username')
    username.send_keys(user_name)
    email = selenium.find_element_by_id('email')
    email.send_keys(f'{user_name}@example.com')
    password = selenium.find_element_by_id('password')
    password.send_keys('p@ssw0rd')
    password_conf = selenium.find_element_by_id('confirm-password')
    password_conf.send_keys('p@ssw0rd')

    submit_button = selenium.find_element_by_tag_name('button')
    submit_button.click()

    assert selenium.current_url == URL
    nav = selenium.find_element_by_tag_name('nav').text
    assert "Register" not in nav
    assert "Log in" not in nav
    assert user_name in nav


def test_register_invalid_email(selenium):
    selenium.get(f"{URL}register")

    menus = selenium.find_elements_by_class_name('menu')
    menus[0].click()

    user_name = random_string()

    username = selenium.find_element_by_id('username')
    username.send_keys(user_name)
    email = selenium.find_element_by_id('email')
    email.send_keys(f'{user_name}')
    password = selenium.find_element_by_id('password')
    password.send_keys('p@ssw0rd')
    password_conf = selenium.find_element_by_id('confirm-password')
    password_conf.send_keys('p@ssw0rd')

    submit_button = selenium.find_element_by_tag_name('button')
    submit_button.click()

    assert selenium.current_url == f"{URL}register"
    nav = selenium.find_element_by_tag_name('nav').text
    assert "Register" in nav
    assert "Log in" in nav


def test_register_password_confirmation_not_ok(selenium):
    selenium.get(f"{URL}register")

    menus = selenium.find_elements_by_class_name('menu')
    menus[0].click()

    user_name = random_string()

    username = selenium.find_element_by_id('username')
    username.send_keys(user_name)
    email = selenium.find_element_by_id('email')
    email.send_keys(f'{user_name}@example.com')
    password = selenium.find_element_by_id('password')
    password.send_keys('p@ssw0rd')
    password_conf = selenium.find_element_by_id('confirm-password')
    password_conf.send_keys('password')

    submit_button = selenium.find_element_by_tag_name('button')
    submit_button.click()

    assert selenium.current_url == f"{URL}register"
    nav = selenium.find_element_by_tag_name('nav').text
    assert "Register" in nav
    assert "Log in" in nav

    errors = selenium.find_element_by_class_name('alert-danger').text
    assert "Password and password confirmation don't match" in errors
