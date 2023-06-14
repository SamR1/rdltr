from unittest.mock import Mock
from urllib import parse

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from rdltr.tests.utils import URL, register_valid_user


def add_valid_article_with_tag(selenium: WebDriver, url: str) -> str:
    menus = selenium.find_elements(By.CLASS_NAME, 'menu')
    menus[3].click()

    link = selenium.find_element(By.ID, 'link')
    link.send_keys(url)
    select = Select(selenium.find_element(By.ID, 'categories'))
    select.select_by_visible_text('default')
    tag = selenium.find_element(By.CLASS_NAME, 'multiselect__input')
    tag.send_keys('test_tag')
    span = selenium.find_element(
        By.CLASS_NAME, 'multiselect__option--highlight'
    )
    span.click()
    submit_button = selenium.find_element(By.TAG_NAME, 'button')
    submit_button.click()
    return url


def check_article(selenium: WebDriver, article_url: str) -> None:
    WebDriverWait(selenium, 10).until(EC.url_matches(f'{URL}articles'))
    assert (
        selenium.find_element(By.CLASS_NAME, 'badge-rdltr').text == 'default'
    )
    assert selenium.find_element(By.TAG_NAME, 'h1').text == 'this is a title'
    assert (
        article_url
        in selenium.find_element(By.CLASS_NAME, 'article-data').text
    )
    assert (
        selenium.find_element(By.ID, 'article-content').text
        == 'this is a paragraph'
    )


def test_add_article_no_category_no_tag(
    selenium: WebDriver, mock_server: Mock
) -> None:
    register_valid_user(selenium)

    menus = selenium.find_elements(By.CLASS_NAME, 'menu')
    menus[3].click()

    url = f'http://localhost:{mock_server.port}/html_ok'
    link = selenium.find_element(By.ID, 'link')
    link.send_keys(url)

    submit_button = selenium.find_element(By.TAG_NAME, 'button')
    submit_button.click()

    check_article(selenium, url)


def test_add_article_with_category_and_tag(
    selenium: WebDriver, mock_server: Mock
) -> None:
    register_valid_user(selenium)
    url = f'http://localhost:{mock_server.port}/html_ok'
    add_valid_article_with_tag(selenium, url)

    WebDriverWait(selenium, 10).until(EC.url_changes(f'{URL}articles/add'))
    assert (
        selenium.find_element(By.CLASS_NAME, 'badge-rdltr').text == 'default'
    )
    assert selenium.find_element(By.TAG_NAME, 'h1').text == 'this is a title'
    assert (
        selenium.find_element(By.CLASS_NAME, 'badge-rdltr-tag').text
        == 'test_tag'
    )
    assert url in selenium.find_element(By.CLASS_NAME, 'article-data').text
    assert (
        selenium.find_element(By.ID, 'article-content').text
        == 'this is a paragraph'
    )


def test_add_article_empty_document(
    selenium: WebDriver, mock_server: Mock
) -> None:
    register_valid_user(selenium)

    menus = selenium.find_elements(By.CLASS_NAME, 'menu')
    menus[3].click()

    url = f'http://localhost:{mock_server.port}'
    link = selenium.find_element(By.ID, 'link')
    link.send_keys(url)
    submit_button = selenium.find_element(By.TAG_NAME, 'button')
    submit_button.click()

    errors = selenium.find_element(By.CLASS_NAME, 'alert-danger').text
    assert 'Error. Cannot parse the document.' in errors


def test_add_article_invalid_url(selenium: WebDriver) -> None:
    register_valid_user(selenium)

    menus = selenium.find_elements(By.CLASS_NAME, 'menu')
    menus[3].click()

    url = 'http://not-existing-url.not'
    link = selenium.find_element(By.ID, 'link')
    link.send_keys(url)
    submit_button = selenium.find_element(By.TAG_NAME, 'button')
    submit_button.click()

    selenium.implicitly_wait(1)
    errors = selenium.find_element(By.CLASS_NAME, 'alert-danger').text
    assert 'Error. Cannot connect to the URL, please check it.' in errors


def test_add_article_url_not_found(
    selenium: WebDriver, mock_server: Mock
) -> None:
    register_valid_user(selenium)

    menus = selenium.find_elements(By.CLASS_NAME, 'menu')
    menus[3].click()

    url = f'http://localhost:{mock_server.port}/not_found'
    link = selenium.find_element(By.ID, 'link')
    link.send_keys(url)
    submit_button = selenium.find_element(By.TAG_NAME, 'button')
    submit_button.click()

    errors = selenium.find_element(By.CLASS_NAME, 'alert-danger').text
    assert (
        'Error. Cannot get the requested resource, '
        'please check the URL (code: 404)' in errors
    )


def test_home_after_adding_article(
    selenium: WebDriver, mock_server: Mock
) -> None:
    register_valid_user(selenium)
    assert (
        selenium.find_element(By.CLASS_NAME, 'articles-msg').text
        == "No articles. Add one !"
    )

    url = f'http://localhost:{mock_server.port}/html_ok'
    add_valid_article_with_tag(selenium, url)

    selenium.get(f"{URL}")
    WebDriverWait(selenium, 10).until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, 'articles-msg'), '1 article'
        )
    )

    card = selenium.find_element(By.CLASS_NAME, 'card')
    assert 'default' in card.find_element(By.CLASS_NAME, 'badge-rdltr').text
    assert (
        'this is a title'
        in card.find_element(By.CLASS_NAME, 'card-title').text
    )
    assert (
        'test_tag' in card.find_element(By.CLASS_NAME, 'badge-rdltr-tag').text
    )

    assert 'page 1 / 1' in selenium.find_element(By.ID, 'pagination').text


def test_add_article_from_bookmark(
    selenium: WebDriver, mock_server: Mock
) -> None:
    register_valid_user(selenium)
    bookmark_url = f'http://localhost:{mock_server.port}/html_ok'
    rdltr_url = f"{URL}bookmarklet?url={parse.quote(bookmark_url)}"
    selenium.get(rdltr_url)
    check_article(selenium, bookmark_url)


def test_add_article_from_bookmark_unauthenticated_user(
    selenium: WebDriver, mock_server: Mock
) -> None:
    user_infos = register_valid_user(selenium)
    menus = selenium.find_elements(By.CLASS_NAME, 'menu')
    menus[2].click()

    bookmark_url = f'http://localhost:{mock_server.port}/html_ok'
    selenium.get(f"{URL}bookmarklet?url={parse.quote(bookmark_url)}")

    email = selenium.find_element(By.ID, 'email')
    email.send_keys(user_infos.get('email'))
    password = selenium.find_element(By.ID, 'password')
    password.send_keys(user_infos.get('password'))
    submit_button = selenium.find_element(By.TAG_NAME, 'button')
    submit_button.click()
    selenium.implicitly_wait(1)
    check_article(selenium, bookmark_url)
