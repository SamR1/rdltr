import re
from typing import Dict, Tuple

import requests
from flask import Blueprint, request
from readability.readability import Unparseable
from requests import ConnectionError
from sqlalchemy import exc, or_

from .. import app_log, db
from ..users.utils import authenticate
from .articles_utils import (
    URLException,
    get_article_content,
    get_article_html_content_from_url,
    is_article_url_valid,
    remove_tracking,
)
from .model import Article, Category, Tag

articles_blueprint = Blueprint('articles', __name__)


@articles_blueprint.route('/articles', methods=['GET'])
@authenticate
def get_user_articles(user_id: int) -> Tuple[Dict, int]:
    params = request.args.copy()
    tag_id = params.get('tag_id')
    page = int(params.get('page', 1))
    category_id = params.get('cat_id')
    query = params.get('q')
    only_not_read = params.get('not_read')
    only_favorites = params.get('favorites')
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
            Article.favorite == True if only_favorites else True,  # noqa
            Category.user_id == user_id,
            Category.id == category_id if category_id else True,
            Article.tags.any(id=tag_id) if tag_id else True,
        )
        .order_by(Article.date_added.desc())
        .paginate(page, 12, False)
    )

    articles = articles_pagination.items
    response_object: Dict = {
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
    return response_object, 200


@articles_blueprint.route('/articles/<int:article_id>', methods=['GET'])
@authenticate
def get_user_article(user_id: int, article_id: int) -> Tuple[Dict, int]:
    article = Article.query.filter_by(id=article_id).first()
    if not article or article.category.user_id != user_id:
        response_object: Dict = {
            'status': 'not found',
            'message': 'Article not found.',
        }
        return response_object, 404

    response_object = {'status': 'success', 'data': [article.serialize()]}
    return response_object, 200


@articles_blueprint.route('/articles', methods=['POST'])
@authenticate
def add_user_article(user_id: int) -> Tuple[Dict, int]:
    post_data = request.get_json()
    if not post_data or post_data.get('url') is None:
        response_object: Dict = {
            'status': 'error',
            'message': 'Invalid payload.',
        }
        return response_object, 400

    url = post_data.get('url').strip()
    url = remove_tracking(url)
    # html content from web browser
    if post_data.get('html_content'):
        html_content = re.sub('class=".*?"', '', post_data.get('html_content'))
        title = post_data.get('title', 'No title')
        article_content = get_article_content(html_content, title)
    # html content from server side
    else:
        if not is_article_url_valid(url):
            response_object = {
                'status': 'error',
                'message': 'Error: Invalid URL, please check it.',
            }
            return response_object, 400

        try:
            html_content = get_article_html_content_from_url(url)
            article_content = get_article_content(html_content)
        except (ConnectionError, requests.exceptions.MissingSchema) as e:
            app_log.error(e)
            response_object = {
                'status': 'error',
                'message': 'Error. Cannot connect to the URL, '
                'please check it.',
            }
            return response_object, 500
        except URLException as e:
            app_log.error(e)
            response_object = {'status': 'error', 'message': str(e)}
            return response_object, 500
        except Unparseable as e:
            app_log.error(e)
            response_object = {
                'status': 'error',
                'message': 'Error. Cannot parse the document.',
            }
            return response_object, 500

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
        return response_object, 500

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
    return response_object, 201


@articles_blueprint.route('/articles/<int:article_id>', methods=['PATCH'])
@authenticate
def update_user_category(user_id: int, article_id: int) -> Tuple[Dict, int]:
    post_data = request.get_json()
    if not post_data:
        response_object: Dict = {
            'status': 'error',
            'message': 'Invalid payload.',
        }
        return response_object, 400

    article = Article.query.filter_by(id=article_id).first()
    if not article or article.category.user_id != user_id:
        response_object = {
            'status': 'not found',
            'message': 'Article not found.',
        }
        return response_object, 404

    category_id = post_data.get('category_id')
    if category_id:
        category = Category.query.filter_by(id=category_id).first()
        if not category or category.user_id != user_id:
            response_object = {
                'status': 'error',
                'message': 'Article category not found.',
            }
            return response_object, 500
        article.category_id = category.id
    try:
        comments = post_data.get('comments')
        if comments:
            article.comments = comments
        read_status = post_data.get('update_read_status')
        if read_status is not None:
            article.read_status = read_status
        favorite = post_data.get('update_favorite')
        if favorite is not None:
            article.favorite = favorite
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
            html_content = get_article_html_content_from_url(article.url)
            article_content = get_article_content(html_content)
            article.title = article_content['title']
            article.content = article_content['content']
            article.html_content = article_content['html_content']
        db.session.commit()
        response_object = {'status': 'success', 'data': [article.serialize()]}
        return response_object, 200
    except (ConnectionError, requests.exceptions.MissingSchema) as e:
        app_log.error(e)
        response_object = {
            'status': 'error',
            'message': 'Error. Cannot connect to the URL, please check it.',
        }
        return response_object, 500
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
        return response_object, 500


@articles_blueprint.route('/articles/<int:article_id>', methods=['DELETE'])
@authenticate
def delete_user_category(user_id: int, article_id: int) -> Tuple[Dict, int]:
    article = Article.query.filter_by(id=article_id).first()
    if not article or article.category.user_id != user_id:
        response_object = {
            'status': 'not found',
            'message': 'Article not found.',
        }
        return response_object, 404
    db.session.delete(article)
    db.session.commit()
    response_object = {'status': 'no content'}
    return response_object, 204
