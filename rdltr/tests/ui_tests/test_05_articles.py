from rdltr.tests.utils import URL, register_valid_user
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_add_article_no_category_no_tag(selenium, mock_server):
    register_valid_user(selenium)

    menus = selenium.find_elements_by_class_name('menu')
    menus[3].click()

    url = 'http://localhost:{port}/html_ok'.format(port=mock_server.port)
    link = selenium.find_element_by_id('link')
    link.send_keys(url)

    submit_button = selenium.find_element_by_tag_name('button')
    submit_button.click()

    WebDriverWait(selenium, 10).until(EC.url_changes(f'{URL}articles/add'))
    assert selenium.find_element_by_tag_name('h1').text == 'this is a title'
    assert (
        selenium.find_element_by_class_name('article-link').text
        == f'Link: {url}'
    )
    assert (
        selenium.find_element_by_id('article-content').text
        == 'this is a paragraph'
    )
