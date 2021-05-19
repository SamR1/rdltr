from rdltr.tests.utils import URL
from selenium.webdriver.remote.webdriver import WebDriver


def test_index_ok(selenium: WebDriver) -> None:
    selenium.get(URL)

    header = selenium.find_element_by_tag_name('header')
    logo = header.find_element_by_class_name('logo').text
    assert 'rdltr a simple "read-it later"' in logo

    nav = header.find_element_by_tag_name('nav').text
    assert 'Register' in nav
    assert 'Log in' in nav

    connexion_form = selenium.find_element_by_id('actionType').text
    assert 'Email' in connexion_form
    assert 'Password' in connexion_form
