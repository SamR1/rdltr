import os

URL = (
    f"http://{os.getenv('RDLTR_HOST', '0.0.0.0')}:"
    f"{os.getenv('RDLTR_PORT', '5000')}"
)


def test_home(selenium):
    selenium.get(URL)

    header = selenium.find_element_by_tag_name('header')
    logo = header.find_element_by_class_name('logo').text
    assert "rdltr a simple \"read-it later\"" in logo
