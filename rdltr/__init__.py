import logging
import os

from flask import Flask

log_file = os.getenv('APP_LOG')
logging.basicConfig(filename=log_file,
                    format=('%(asctime)s - %(name)s - %(levelname)s - '
                            '%(message)s'),
                    datefmt='%Y/%m/%d %H:%M:%S')
app_log = logging.getLogger('rdltr')


def create_app():
    app = Flask(__name__)
    app_log.setLevel(logging.DEBUG if app.debug else logging.INFO)

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    return app
