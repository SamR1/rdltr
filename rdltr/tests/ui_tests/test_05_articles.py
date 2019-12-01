from rdltr.tests.utils import URL, register_valid_user
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def test_add_article_no_category_no_tag(selenium, mock_server):
    register_valid_user(selenium)

    menus = selenium.find_elements_by_class_name('menu')
    menus[3].click()

    url = f'http://localhost:{mock_server.port}/html_ok'
    link = selenium.find_element_by_id('link')
    link.send_keys(url)

    submit_button = selenium.find_element_by_tag_name('button')
    submit_button.click()

    WebDriverWait(selenium, 10).until(EC.url_changes(f'{URL}articles/add'))
    assert selenium.find_element_by_class_name('badge-rdltr').text == 'default'
    assert selenium.find_element_by_tag_name('h1').text == 'this is a title'
    assert (
        selenium.find_element_by_class_name('article-link').text
        == f'Link: {url}'
    )
    assert (
        selenium.find_element_by_id('article-content').text
        == 'this is a paragraph'
    )


def test_add_article_with_category_and_tag(selenium, mock_server):
    register_valid_user(selenium)

    menus = selenium.find_elements_by_class_name('menu')
    menus[3].click()

    url = f'http://localhost:{mock_server.port}/html_ok'
    link = selenium.find_element_by_id('link')
    link.send_keys(url)
    select = Select(selenium.find_element_by_id('categories'))
    select.select_by_visible_text('default')
    tag = selenium.find_element_by_class_name('multiselect__input')
    tag.send_keys('test_tag')
    span = selenium.find_element_by_class_name(
        'multiselect__option--highlight'
    )
    span.click()
    submit_button = selenium.find_element_by_tag_name('button')
    submit_button.click()

    WebDriverWait(selenium, 10).until(EC.url_changes(f'{URL}articles/add'))
    assert selenium.find_element_by_class_name('badge-rdltr').text == 'default'
    assert selenium.find_element_by_tag_name('h1').text == 'this is a title'
    assert (
        selenium.find_element_by_class_name('badge-rdltr-tag').text
        == 'test_tag'
    )
    assert (
        selenium.find_element_by_class_name('article-link').text
        == f'Link: {url}'
    )
    assert (
        selenium.find_element_by_id('article-content').text
        == 'this is a paragraph'
    )


def test_add_article_empty_document(selenium, mock_server):
    register_valid_user(selenium)

    menus = selenium.find_elements_by_class_name('menu')
    menus[3].click()

    url = f'http://localhost:{mock_server.port}'
    link = selenium.find_element_by_id('link')
    link.send_keys(url)
    submit_button = selenium.find_element_by_tag_name('button')
    submit_button.click()

    errors = selenium.find_element_by_class_name('alert-danger').text
    assert 'Error. Cannot parse the document.' in errors


def test_add_article_invalid_url(selenium):
    register_valid_user(selenium)

    menus = selenium.find_elements_by_class_name('menu')
    menus[3].click()

    url = 'http://not-existing-url.not'
    link = selenium.find_element_by_id('link')
    link.send_keys(url)
    submit_button = selenium.find_element_by_tag_name('button')
    submit_button.click()

    errors = selenium.find_element_by_class_name('alert-danger').text
    assert 'Error. Cannot connect to the URL, please check it.' in errors


def test_add_article_url_not_found(selenium, mock_server):
    register_valid_user(selenium)

    menus = selenium.find_elements_by_class_name('menu')
    menus[3].click()

    url = f'http://localhost:{mock_server.port}/not_found'
    link = selenium.find_element_by_id('link')
    link.send_keys(url)
    submit_button = selenium.find_element_by_tag_name('button')
    submit_button.click()

    errors = selenium.find_element_by_class_name('alert-danger').text
    assert (
        'Error. Cannot get the requested resource, '
        'please check the URL (code: 404)' in errors
    )
