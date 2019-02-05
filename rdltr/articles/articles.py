import requests
from flask import Blueprint, jsonify, request
from readability import Document

from .. import app_log, db
from ..users.utils import authenticate
from .model import Article, Category

articles_blueprint = Blueprint('articles', __name__)


@articles_blueprint.route('/articles', methods=['GET'])
@authenticate
def get_user_articles(user_id):
    articles = Article.query.filter_by(id=user_id).all()
    response_object = {
        'status': 'success',
        'data': [article.serialize() for article in articles],
    }
    return jsonify(response_object), 200


@articles_blueprint.route('/articles', methods=['POST'])
@authenticate
def add_user_article(user_id):
    post_data = request.get_json()
    if not post_data or post_data.get('url') is None:
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400

    url = post_data.get('url')

    try:
        response = requests.get(url)
        doc = Document(response.text)
        title = doc.title()
        content = doc.content()
    except Exception as e:
        app_log.error(e)
        response_object = {
            'status': 'error',
            'message': 'Error. Please try again or contact the administrator.',
        }
        return jsonify(response_object), 500

    category_id = post_data.get('category_id')
    if not category_id:
        category = Category.query.filter_by(
            user_id=user_id, is_default=True
        ).first()
    else:
        category = Category.query.filter_by(id=category_id).first()

    if not category:
        response_object = {
            'status': 'error',
            'message': 'Article category not found.',
        }
        return jsonify(response_object), 500

    new_article = Article(
        category_id=category.id, title=title, content=content, url=url
    )
    # TODO: tags
    db.session.add(new_article)
    db.session.commit()
    response_object = {'status': 'success', 'data': [new_article.serialize()]}
    return jsonify(response_object), 201
