import logging
import os

from flask import Flask, jsonify, render_template
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

log_file = os.getenv('RDLTR_LOG')
logging.basicConfig(
    filename=log_file,
    format='%(asctime)s - %(name)s - %(levelname)s - ' '%(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
)
app_log = logging.getLogger('rdltr')
bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, static_folder="dist/static", template_folder="dist")
    app_log.setLevel(logging.DEBUG if app.debug else logging.INFO)

    # set config
    with app.app_context():
        app_settings = os.getenv(
            'RDLTR_SETTINGS', 'rdltr.config.DevelopmentConfig'
        )
        app.config.from_object(app_settings)

        # set up extensions
        bcrypt.init_app(app)
        db.init_app(app)
        migrate.init_app(app, db, directory='rdltr/migrations')

    if app.debug:
        logging.getLogger('sqlalchemy').setLevel(logging.WARNING)
        logging.getLogger('sqlalchemy').handlers = logging.getLogger(
            'werkzeug'
        ).handlers
        logging.getLogger('sqlalchemy.orm').setLevel(logging.WARNING)
        logging.getLogger('flake8').propagate = False
        app_log.setLevel(logging.DEBUG)

    if app.debug:
        # Enable CORS
        @app.after_request
        def after_request(response):
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add(
                'Access-Control-Allow-Headers', 'Content-Type,Authorization'
            )
            response.headers.add(
                'Access-Control-Allow-Methods',
                'GET,PUT,POST,DELETE,PATCH,OPTIONS',
            )
            return response

    from .articles.model import Article, Category, Tag  # noqa
    from .users.model import User  # noqa

    from .articles.articles import articles_blueprint  # noqa
    from .articles.categories import categories_blueprint  # noqa
    from .articles.tags import tags_blueprint  # noqa
    from .users.auth import auth_blueprint  # noqa

    app.register_blueprint(articles_blueprint, url_prefix='/api')
    app.register_blueprint(auth_blueprint, url_prefix='/api')
    app.register_blueprint(categories_blueprint, url_prefix='/api')
    app.register_blueprint(tags_blueprint, url_prefix='/api')

    @app.route('/api/ping')
    def ping_pong():
        return jsonify({'status': 'success', 'message': 'pong!'})

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return render_template('index.html')

    return app
