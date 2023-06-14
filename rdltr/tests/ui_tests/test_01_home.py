from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from rdltr.tests.utils import URL


def test_index_ok(selenium: WebDriver) -> None:
    selenium.get(URL)

    header = selenium.find_element(By.TAG_NAME, "header")
    logo = header.find_element(By.CLASS_NAME, "logo").text
    assert 'rdltr a simple "read-it later"' in logo

    nav = header.find_element(By.TAG_NAME, "nav").text
    assert "Register" in nav
    assert "Log in" in nav

    connexion_form = selenium.find_element(By.ID, "actionType").text
    assert "Email" in connexion_form
    assert "Password" in connexion_form
