from unittest.mock import Mock


def mock_api(html):
    mock_response = Mock()
    mock_response.return_value = html
    return mock_response


class MockResponse:
    def __init__(self, html_content):
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

html_doc_body_ok = (
    "b'<body>\\n        <p>this is a paragraph</p>\\n    </body>\\n'"
)

mock_response_ok = MockResponse(html_doc_ok)
mock_response_ko = MockResponse('')
