import json
import os
import random
import string

URL = (
    f"http://{os.getenv('RDLTR_HOST', '0.0.0.0')}:"
    f"{os.getenv('RDLTR_PORT', '5000')}/"
)


def check_400_invalid_payload(response):
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert data['message'] == 'Invalid payload.'


def check_400_invalid_credentials(response):
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert data['message'] == 'Invalid credentials.'


def check_500_error(response):
    assert response.content_type == 'application/json'
    assert response.status_code == 500
    data = json.loads(response.data.decode())
    assert data['status'] == 'error'
    assert (
        'Error. Please try again or contact the administrator.'
        in data['message']
    )


def random_string(length=8):
    return ''.join(random.choice(string.ascii_letters) for x in range(length))


def register(selenium, user_infos):
    selenium.get(f"{URL}register")
    nav = selenium.find_element_by_tag_name('nav')
    menus = nav.find_elements_by_class_name('menu')
    assert "Register" in menus[0].text
    menus[0].click()

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


def login(selenium, user_infos, redirect_to_url=False):
    if redirect_to_url:
        selenium.get(f"{URL}login")
    menus = selenium.find_elements_by_class_name('menu')
    assert "Log in" in menus[1].text
    menus[1].click()

    email = selenium.find_element_by_id('email')
    email.send_keys(user_infos.get('email'))
    password = selenium.find_element_by_id('password')
    password.send_keys(user_infos.get('password'))

    submit_button = selenium.find_element_by_tag_name('button')
    submit_button.click()


def register_valid_user(selenium):
    user_name = random_string()
    user_infos = {
        'username': user_name,
        'email': f'{user_name}@example.com',
        'password': 'p@ssw0rd',
        'password_conf': 'p@ssw0rd',
    }
    register(selenium, user_infos)
    return user_infos
