from rdltr.tests.utils import URL, register_valid_user


def fill_form(selenium, form_values, is_category=True):
    name = selenium.find_element_by_id('name')
    name.clear()
    name.send_keys(form_values['name'])
    if is_category:
        description = selenium.find_element_by_id('description')
        description.clear()
        description.send_keys(form_values['description'])
    submit_button = selenium.find_element_by_tag_name('button')
    submit_button.click()


def test_settings_display_categories(selenium):
    register_valid_user(selenium)
    menus = selenium.find_elements_by_class_name('menu')
    menus[1].click()

    box = selenium.find_element_by_class_name("rdltr-box")
    buttons = box.find_elements_by_tag_name("button")
    assert 'Categories' in buttons[0].text
    assert 'Tags' in buttons[1].text
    assert 'Back to home' in buttons[2].text

    buttons[0].click()

    container = selenium.find_element_by_class_name("container")
    rows = container.find_elements_by_class_name("row")

    buttons = rows[0].find_elements_by_tag_name("button")
    back_to_settings = buttons[0]
    assert 'Back to settings' in back_to_settings.text
    assert 'Add a category' in buttons[1].text

    rows[1].find_elements_by_tag_name("input")
    assert 'Search' in rows[1].find_element_by_tag_name("span").text

    # default category should exist. this category can not be deleted
    table = rows[2].find_element_by_tag_name("table")
    thead_th = table.find_element_by_tag_name(
        "thead"
    ).find_elements_by_tag_name("th")
    assert "Id" in thead_th[0].text
    assert "Name" in thead_th[1].text
    assert "Description" in thead_th[2].text
    assert "Nb articles" in thead_th[3].text
    assert "Action" in thead_th[4].text
    tbody_td = table.find_element_by_tag_name(
        "tbody"
    ).find_elements_by_tag_name("td")
    assert "default" in tbody_td[1].text
    assert (
        len(tbody_td[1].find_elements_by_class_name("badge-rdltr-small")) == 1
    )
    assert "Default category" in tbody_td[2].text
    assert "0" in tbody_td[3].text
    assert len(tbody_td[4].find_elements_by_class_name("fa-trash")) == 0


def test_settings_display_tags(selenium):
    register_valid_user(selenium)
    selenium.get(f"{URL}settings")

    box = selenium.find_element_by_class_name("rdltr-box")
    box.find_elements_by_tag_name("button")[1].click()

    container = selenium.find_element_by_class_name("container")
    rows = container.find_elements_by_class_name("row")

    buttons = rows[0].find_elements_by_tag_name("button")
    back_to_settings = buttons[0]
    assert 'Back to settings' in back_to_settings.text
    assert 'Add a tag' in buttons[1].text

    rows[1].find_elements_by_tag_name("input")
    assert 'Search' in rows[1].find_element_by_tag_name("span").text

    table = rows[2].find_element_by_tag_name("table")
    thead_th = table.find_element_by_tag_name(
        "thead"
    ).find_elements_by_tag_name("th")
    assert "Id" in thead_th[0].text
    assert "Name" in thead_th[1].text
    assert "Nb articles" in thead_th[2].text
    assert "Action" in thead_th[3].text
    tbody_td = table.find_element_by_tag_name(
        "tbody"
    ).find_elements_by_tag_name("td")
    assert tbody_td == []


def test_settings_update_categories(selenium):
    register_valid_user(selenium)
    selenium.get(f"{URL}settings/categories")

    add_button = selenium.find_elements_by_tag_name("button")[1]
    add_button.click()

    # add a category
    form_values = {"name": "news", "description": "News category"}
    fill_form(selenium, form_values)
    tbody_td = selenium.find_element_by_tag_name(
        "tbody"
    ).find_elements_by_tag_name("td")
    assert "default" in tbody_td[1].text
    assert (
        len(tbody_td[1].find_elements_by_class_name("badge-rdltr-small")) == 1
    )
    assert "Default category" in tbody_td[2].text
    assert "0" in tbody_td[3].text
    assert "news" in tbody_td[6].text
    assert tbody_td[6].find_elements_by_class_name("badge-rdltr-small") == []
    assert "News category" in tbody_td[7].text
    assert "0" in tbody_td[8].text
    assert len(tbody_td[9].find_elements_by_class_name("fa-trash")) == 1

    # edit the category
    tbody_td[9].find_element_by_class_name("fa-pencil").click()

    form_values = {
        "name": "sports",
        "description": "All articles about sports",
    }
    fill_form(selenium, form_values)
    tbody_td = selenium.find_element_by_tag_name(
        "tbody"
    ).find_elements_by_tag_name("td")
    assert "default" in tbody_td[1].text
    assert (
        len(tbody_td[1].find_elements_by_class_name("badge-rdltr-small")) == 1
    )
    assert "Default category" in tbody_td[2].text
    assert "0" in tbody_td[3].text
    assert "sports" in tbody_td[6].text
    assert tbody_td[6].find_elements_by_class_name("badge-rdltr-small") == []
    assert "All articles about sports" in tbody_td[7].text
    assert "0" in tbody_td[8].text

    # delete the category
    tbody_td[9].find_element_by_class_name("fa-trash").click()

    tbody_td = selenium.find_element_by_tag_name(
        "tbody"
    ).find_elements_by_tag_name("td")
    assert len(tbody_td) == 5
    assert "default" in tbody_td[1].text
    assert (
        len(tbody_td[1].find_elements_by_class_name("badge-rdltr-small")) == 1
    )
    assert "Default category" in tbody_td[2].text


def test_settings_update_tags(selenium):
    register_valid_user(selenium)
    selenium.get(f"{URL}settings/tags")

    add_button = selenium.find_elements_by_tag_name("button")[1]
    add_button.click()

    # add a tag
    fill_form(selenium, {"name": "python"}, is_category=False)
    tbody_td = selenium.find_element_by_tag_name(
        "tbody"
    ).find_elements_by_tag_name("td")
    assert "python" in tbody_td[1].text
    assert "0" in tbody_td[2].text
    edit_icon = tbody_td[3].find_element_by_class_name("fa-pencil")
    assert len(tbody_td[3].find_elements_by_class_name("fa-trash")) == 1

    # edit the tag
    edit_icon.click()

    fill_form(selenium, {"name": "tests"}, is_category=False)
    tbody_td = selenium.find_element_by_tag_name(
        "tbody"
    ).find_elements_by_tag_name("td")
    assert "tests" in tbody_td[1].text

    # delete the tag
    tbody_td[3].find_element_by_class_name("fa-trash").click()

    tbody_td = selenium.find_element_by_tag_name(
        "tbody"
    ).find_elements_by_tag_name("td")
    assert tbody_td == []
