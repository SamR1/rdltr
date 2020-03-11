from unittest.mock import patch

import pytest
from rdltr.articles.articles_utils import (
    URLException,
    get_article_content,
    get_article_html_content_from_url,
    is_article_url_valid,
)

from ..utils_requests import html_doc_body_ok, html_doc_ok


@patch('requests.get')
def test_it_returns_html_content(get_mock, mock_request_ok):
    get_mock.return_value = mock_request_ok.return_value
    result = get_article_html_content_from_url('https://example.com')
    assert result == html_doc_ok


@patch('requests.get')
@pytest.mark.xfail(raises=URLException)
def test_it_returns_exception_on_requests_error(
    get_mock, mock_request_not_found
):
    get_mock.return_value = mock_request_not_found.return_value
    get_article_html_content_from_url('https://example.com')


@patch('requests.get')
def test_it_returns_html_content_on_different_encoding(
    get_mock, mock_request_different_encoding
):
    get_mock.return_value = mock_request_different_encoding.return_value
    result = get_article_html_content_from_url('https://example.com')
    assert result == html_doc_ok


def test_it_return_clean_content():
    result = get_article_content(html_doc_ok)
    assert result['title'] == 'this is a title'
    assert result['content'] == '\nthis is a paragraph\n\n'
    assert result['html_content'] == html_doc_body_ok


def test_it_return_clean_content_with_provided_title():
    result = get_article_content(html_doc_ok, title='new title')
    assert result['title'] == 'new title'
    assert result['content'] == '\nthis is a paragraph\n\n'
    assert result['html_content'] == html_doc_body_ok


def test_it_returns_false_when_url_is_invalid():
    url = 'htt://www.example.com'
    assert not is_article_url_valid(url)


def test_it_returns_true_when_url_is_valid():
    url = 'https://www.example.com'
    assert is_article_url_valid(url)
