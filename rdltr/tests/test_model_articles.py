def test_category_model(app, user_1, cat_1):
    assert 1 == cat_1.id
    assert 1 == cat_1.user_id
    assert 'python' == cat_1.name
    assert not cat_1.description
    assert cat_1.is_default is False

    serialized_cat = cat_1.serialize()
    assert 1 == serialized_cat['id']
    assert 1 == serialized_cat['user_id']
    assert 'python' == serialized_cat['name']
    assert not serialized_cat['description']
    assert serialized_cat['is_default'] is False


def test_category_2_model(app, user_1, user_2, cat_2):
    assert 1 == cat_2.id
    assert 2 == cat_2.user_id
    assert 'moto' == cat_2.name
    assert 'related to motorcycles' == cat_2.description
    assert cat_2.is_default is False

    serialized_cat = cat_2.serialize()
    assert 1 == serialized_cat['id']
    assert 2 == serialized_cat['user_id']
    assert 'moto' == serialized_cat['name']
    assert 'related to motorcycles' == serialized_cat['description']
    assert serialized_cat['is_default'] is False


def test_tag_model(app, user_1, tag_1):
    assert 1 == tag_1.id
    assert 1 == tag_1.user_id
    assert 'tips' == tag_1.name

    serialized_tag = tag_1.serialize()
    assert 1 == serialized_tag['id']
    assert 1 == serialized_tag['user_id']
    assert 'tips' == serialized_tag['name']


def test_article_1_model(app, user_1, cat_1, article_1):
    assert 1 == article_1.id
    assert 1 == article_1.category_id
    assert 'Python tips' == article_1.title
    assert 'Test' == article_1.content
    assert (
        '<html><head><title>Titre</head><body><p>Test</p></body></html>'
        == article_1.html_content
    )
    assert 'https://test.com' == article_1.url
    assert not article_1.comments
    assert 2 == len(article_1.tags)
    assert 'tips' == article_1.tags[0].name
    assert article_1.date_added
    assert not article_1.read_status
    assert not article_1.favorite

    serialized_article = article_1.serialize()
    assert 1 == serialized_article['id']
    assert 'Python tips' == serialized_article['title']
    assert (
        '<html><head><title>Titre</head><body><p>Test</p></body></html>'
        == serialized_article['html_content']
    )
    assert 'https://test.com' == serialized_article['url']
    assert not serialized_article['comments']
    assert 'tips' == serialized_article['tags'][0]['name']
    assert 1 == serialized_article['category']['id']
    assert 'date_added' in serialized_article
    assert not serialized_article['read']
    assert not serialized_article['favorite']


def test_article_2_model(app, user_1, cat_1, article_2):
    assert 1 == article_2.id
    assert 1 == article_2.category_id
    assert 'Another article' == article_2.title
    assert 'Test2' == article_2.content
    assert (
        '<html><head><title>Titre2</head><body><p>Test2</p></body></html>'
        == article_2.html_content
    )
    assert 'https://test.com' == article_2.url
    assert 'just a comment' == article_2.comments
    assert 0 == len(article_2.tags)
    assert article_2.date_added
    assert article_2.read_status
    assert article_2.favorite

    serialized_article = article_2.serialize()
    assert 1 == serialized_article['id']
    assert 'Another article' == serialized_article['title']
    assert (
        '<html><head><title>Titre2</head><body><p>Test2</p></body></html>'
        == serialized_article['html_content']
    )
    assert 'https://test.com' == serialized_article['url']
    assert 'just a comment' == serialized_article['comments']
    assert [] == serialized_article['tags']
    assert 1 == serialized_article['category']['id']
    assert 'date_added' in serialized_article
    assert serialized_article['read']
    assert serialized_article['favorite']
