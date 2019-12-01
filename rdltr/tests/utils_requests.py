from unittest.mock import Mock


def mock_api(html):
    mock_response = Mock()
    mock_response.return_value = html
    return mock_response


class MockResponse:
    def __init__(self, html_content, code=200):
        self.status_code = code
        self.text = html_content


html_doc_ok = """
<html>
    <head>
    <title>this is a title</title>
    </head>
    <body>
        <p>this is a paragraph</p>
    </body>
</html>
"""

html_doc_body_ok = """<body id="readabilityBody">
        <p>this is a paragraph</p>
    </body>
"""

mock_response_empty = MockResponse('')
mock_response_not_found = MockResponse('', code=404)
mock_response_ok = MockResponse(html_doc_ok)
