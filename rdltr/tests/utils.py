import json
import os
import random
import string
from typing import Dict

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from werkzeug.test import TestResponse

URL = (
    f"http://{os.getenv('RDLTR_HOST', '0.0.0.0')}:"
    f"{os.getenv('RDLTR_PORT', '5000')}/"
)


def check_400_invalid_payload(response: TestResponse) -> None:
    assert response.content_type == "application/json"
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == "error"
    assert data["message"] == "Invalid payload."


def check_400_invalid_credentials(response: TestResponse) -> None:
    assert response.content_type == "application/json"
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == "error"
    assert data["message"] == "Invalid credentials."


def check_500_error(response: TestResponse) -> None:
    assert response.content_type == "application/json"
    assert response.status_code == 500
    data = json.loads(response.data.decode())
    assert data["status"] == "error"
    assert (
        "Error. Please try again or contact the administrator."
        in data["message"]
    )


def random_string(length: int = 8) -> str:
    return "".join(random.choice(string.ascii_letters) for x in range(length))


def register(selenium: WebDriver, user_infos: Dict) -> None:
    selenium.get(f"{URL}register")
    menus = selenium.find_elements(By.CLASS_NAME, "menu")
    assert "Register" in menus[0].text
    menus[0].click()

    username = selenium.find_element(By.ID, "username")
    username.send_keys(user_infos.get("username"))
    email = selenium.find_element(By.ID, "email")
    email.send_keys(user_infos.get("email"))
    password = selenium.find_element(By.ID, "password")
    password.send_keys(user_infos.get("password"))
    password_conf = selenium.find_element(By.ID, "confirm-password")
    password_conf.send_keys(user_infos.get("password_conf"))

    submit_button = selenium.find_element(By.TAG_NAME, "button")
    submit_button.click()


def login(
    selenium: WebDriver, user_infos: Dict, redirect_to_url: bool = False
) -> None:
    if redirect_to_url:
        selenium.get(f"{URL}login")
    menus = selenium.find_elements(By.CLASS_NAME, "menu")
    assert "Log in" in menus[1].text
    menus[1].click()

    email = selenium.find_element(By.ID, "email")
    email.send_keys(user_infos.get("email"))
    password = selenium.find_element(By.ID, "password")
    password.send_keys(user_infos.get("password"))

    submit_button = selenium.find_element(By.TAG_NAME, "button")
    submit_button.click()


def register_valid_user(selenium: WebDriver) -> Dict:
    user_name = random_string()
    user_infos = {
        "username": user_name,
        "email": f"{user_name}@example.com",
        "password": "p@ssw0rd",
        "password_conf": "p@ssw0rd",
    }
    register(selenium, user_infos)
    WebDriverWait(selenium, 10).until(EC.url_changes(f"{URL}register"))
    return user_infos


def login_valid_user(selenium: WebDriver, user_infos: Dict) -> Dict:
    login(selenium, user_infos)
    WebDriverWait(selenium, 10).until(EC.url_changes(f"{URL}login"))
    return user_infos
