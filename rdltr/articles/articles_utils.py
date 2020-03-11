import re

import requests
from bs4 import BeautifulSoup
from readability import Document


TRACKING_REMOVAL_REGEXES = [
    re.compile(r'utm_[^&]+&?'),
    re.compile(r'&$'),
    re.compile(r'\?$'),
]


class URLException(Exception):
    ...


def get_article_html_content_from_url(url):
    headers = {'User-Agent': 'Mozilla/5.0'}  # to avoid 403
    response = requests.get(url, headers=headers)
    if response.status_code >= 400:
        raise URLException(
            'Error. Cannot get the requested resource, please check '
            f'the URL (code: {response.status_code})'
        )
    if not response.encoding or (
        response.apparent_encoding.lower() != response.encoding.lower()
        and response.apparent_encoding.lower() == 'utf-8'
    ):
        response.encoding = response.apparent_encoding
    return response.text


def get_article_content(html_content, title=None):
    doc = Document(html_content)
    # 'html_content' is used for display
    # and existing classes are removed
    html_content = re.sub('class=".*?"', '', doc.summary(html_partial=False))
    # 'content' is used for search
    content = BeautifulSoup(html_content, "html.parser").text
    return {
        'title': title if title else doc.title(),
        'content': content,
        'html_content': html_content,
    }


def is_article_url_valid(url):
    # regex from Django validator
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # noqa
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE,
    )
    return re.match(regex, url)


def remove_tracking(url):
    for regex in TRACKING_REMOVAL_REGEXES:
        url = regex.sub('', url)
    return url
