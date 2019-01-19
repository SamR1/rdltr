import logging
import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


log_file = os.getenv('APP_LOG')
logging.basicConfig(
    filename=log_file,
    format='%(asctime)s - %(name)s - %(levelname)s - ' '%(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
)
app_log = logging.getLogger('rdltr')
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app_log.setLevel(logging.DEBUG if app.debug else logging.INFO)

    # set config
    with app.app_context():
        app_settings = os.getenv('APP_SETTINGS')
        app.config.from_object(app_settings)

        # set up extensions
        db.init_app(app)
        migrate.init_app(app, db)

    if app.debug:
        logging.getLogger('sqlalchemy').setLevel(logging.WARNING)
        logging.getLogger('sqlalchemy').handlers = logging.getLogger(
            'werkzeug'
        ).handlers
        logging.getLogger('sqlalchemy.orm').setLevel(logging.WARNING)
        logging.getLogger('flake8').propagate = False
        app_log.setLevel(logging.DEBUG)

    from .users.model import User  # noqa

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    return app
