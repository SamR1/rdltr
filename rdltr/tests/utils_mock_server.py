import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

import requests
from rdltr.tests.utils_requests import html_doc_ok


class MockServer(BaseHTTPRequestHandler):
    def do_GET(self):
        message = ''
        if self.path == '/html_ok':
            message = html_doc_ok
        self.send_response(requests.codes.ok)
        self.end_headers()
        self.wfile.write(bytes(message, 'utf-8'))


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


class MockTestServer(Thread):
    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.port = get_free_port()
        self.server = HTTPServer(('localhost', self.port), MockServer)

        self.mock_server_thread = Thread(target=self.server.serve_forever)
        self.mock_server_thread.setDaemon(True)
        self.mock_server_thread.start()

    def close_session(self):
        self.session.close()
