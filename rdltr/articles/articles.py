import re

import requests
from bs4 import BeautifulSoup
from flask import Blueprint, jsonify, request
from readability import Document
from requests import ConnectionError
from sqlalchemy import exc, or_

from .. import app_log, db
from ..users.utils import authenticate
from .model import Article, Category, Tag

articles_blueprint = Blueprint('articles', __name__)


def get_article_content(url):
    headers = {'User-Agent': 'Mozilla/5.0'}  # to avoid 403
    response = requests.get(url, headers=headers)
    doc = Document(response.text)
    # 'html_content' is used for display
    # and existing classes are removed
    html_content = re.sub('class=".*?"', '', doc.summary(html_partial=False))
    # 'content' is used for search
    content = BeautifulSoup(html_content, "html.parser").text
    return {
        'title': doc.title(),
        'content': content,
        'html_content': html_content,
    }


@articles_blueprint.route('/articles', methods=['GET'])
@authenticate
def get_user_articles(user_id):
    params = request.args.copy()
    tag_id = params.get('tag_id')
    page = 1 if 'page' not in params.keys() else int(params.get('page'))
    category_id = params.get('cat_id')
    query = params.get('q')
    only_not_read = params.get('not_read')
    articles_pagination = (
        Article.query.join(Category)
        .filter(
            or_(
                Article.title.like('%' + query + '%'),
                Article.content.like('%' + query + '%'),
            )
            if query
            else True,
            Article.read_status == False if only_not_read else True,  # noqa
            Category.user_id == user_id,
            Category.id == category_id if category_id else True,
            Article.tags.any(id=tag_id) if tag_id else True,
        )
        .order_by(Article.date_added.desc())
        .paginate(page, 12, False)
    )

    articles = articles_pagination.items
    response_object = {
        'status': 'success',
        'data': [article.serialize() for article in articles],
        'pagination': {
            'has_next': articles_pagination.has_next,
            'has_prev': articles_pagination.has_prev,
            'page': articles_pagination.page,
            'pages': articles_pagination.pages,
            'total': articles_pagination.total,
        },
    }
    return jsonify(response_object), 200


@articles_blueprint.route('/articles/<int:article_id>', methods=['GET'])
@authenticate
def get_user_article(user_id, article_id):
    article = Article.query.filter_by(id=article_id).first()
    if not article or article.category.user_id != user_id:
        response_object = {
            'status': 'not found',
            'message': f'Article not found.',
        }
        return jsonify(response_object), 404

    response_object = {'status': 'success', 'data': [article.serialize()]}
    return jsonify(response_object), 200


@articles_blueprint.route('/articles', methods=['POST'])
@authenticate
def add_user_article(user_id):
    post_data = request.get_json()
    if not post_data or post_data.get('url') is None:
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400

    url = post_data.get('url').strip()

    # check if url is valid (regex from Django validator)
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
    if not re.match(regex, url):
        response_object = {
            'status': 'error',
            'message': 'Error: Invalid URL, please check it.',
        }
        return jsonify(response_object), 400

    try:
        article_content = get_article_content(url)
    except (ConnectionError, requests.exceptions.MissingSchema) as e:
        app_log.error(e)
        response_object = {
            'status': 'error',
            'message': 'Error. Cannot connect to the URL, please check it.',
        }
        return jsonify(response_object), 500
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
        category_id=category.id,
        title=article_content['title'],
        content=article_content['content'],
        html_content=article_content['html_content'],
        url=url,
    )
    db.session.flush()
    tags = post_data.get('tags')
    if tags and isinstance(tags, list):
        for tag_name in tags:
            tag = Tag.query.filter_by(user_id=user_id, name=tag_name).first()
            if not tag:
                tag = Tag(user_id=user_id, name=tag_name)
                db.session.flush()
            new_article.tags.append(tag)
            db.session.flush()
    db.session.add(new_article)
    db.session.commit()
    response_object = {'status': 'success', 'data': [new_article.serialize()]}
    return jsonify(response_object), 201


@articles_blueprint.route('/articles/<int:article_id>', methods=['PATCH'])
@authenticate
def update_user_category(user_id, article_id):
    post_data = request.get_json()
    if not post_data:
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400

    article = Article.query.filter_by(id=article_id).first()
    if not article or article.category.user_id != user_id:
        response_object = {
            'status': 'not found',
            'message': f'Article not found.',
        }
        return jsonify(response_object), 404

    category_id = post_data.get('category_id')
    if category_id:
        category = Category.query.filter_by(id=category_id).first()
        if not category or category.user_id != user_id:
            response_object = {
                'status': 'error',
                'message': f'Article category not found.',
            }
            return jsonify(response_object), 500
        article.category_id = category.id
    try:
        comments = post_data.get('comments')
        if comments:
            article.comments = comments
        read_status = post_data.get('update_read_status')
        if read_status is not None:
            article.read_status = read_status
        new_tags = post_data.get('tags')
        if isinstance(new_tags, list):
            if not new_tags:
                article.tags.clear()
            else:
                existing_tags = [tag for tag in article.tags]
                for existing_tag in existing_tags:
                    if existing_tag.name not in new_tags:
                        article.tags.remove(existing_tag)
                        db.session.flush()
                for tag_name in new_tags:
                    tag = Tag.query.filter_by(
                        user_id=user_id, name=tag_name
                    ).first()
                    if not tag:
                        tag = Tag(user_id=user_id, name=tag_name)
                        db.session.flush()
                    article.tags.append(tag)
                    db.session.flush()
        if post_data.get('reload'):
            article_content = get_article_content(article.url)
            article.title = article_content['title']
            article.content = article_content['content']
            article.html_content = article_content['html_content']
        db.session.commit()
        response_object = {'status': 'success', 'data': [article.serialize()]}
        return jsonify(response_object), 200
    except (ConnectionError, requests.exceptions.MissingSchema) as e:
        app_log.error(e)
        response_object = {
            'status': 'error',
            'message': 'Error. Cannot connect to the URL, please check it.',
        }
        return jsonify(response_object), 500
    except (
        exc.IntegrityError,
        exc.OperationalError,
        exc.InterfaceError,
        exc.StatementError,
    ) as e:
        db.session.rollback()
        app_log.error(e)
        response_object = {
            'status': 'error',
            'message': 'Error. Please try again or contact the administrator.',
        }
        return jsonify(response_object), 500


@articles_blueprint.route('/articles/<int:article_id>', methods=['DELETE'])
@authenticate
def delete_user_category(user_id, article_id):
    article = Article.query.filter_by(id=article_id).first()
    if not article or article.category.user_id != user_id:
        response_object = {
            'status': 'not found',
            'message': f'Article not found.',
        }
        return jsonify(response_object), 404
    db.session.delete(article)
    db.session.commit()
    response_object = {'status': 'no content'}
    return jsonify(response_object), 204
