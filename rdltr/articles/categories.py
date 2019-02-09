from flask import Blueprint, jsonify, request

from .. import db
from ..users.utils import authenticate
from .model import Category

categories_blueprint = Blueprint('categories', __name__)


@categories_blueprint.route('/categories', methods=['GET'])
@authenticate
def get_user_categories(user_id):
    categories = Category.query.filter_by(id=user_id).all()
    response_object = {
        'status': 'success',
        'data': [category.serialize() for category in categories],
    }
    return jsonify(response_object), 200


@categories_blueprint.route('/categories', methods=['POST'])
@authenticate
def add_user_category(user_id):
    post_data = request.get_json()
    if not post_data or post_data.get('name') is None:
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400

    name = post_data.get('name').lower()
    category = Category.query.filter_by(user_id=user_id, name=name).first()
    if category:
        response_object = {
            'status': 'error',
            'message': f'A category named "{name}" already exists.',
        }
        return jsonify(response_object), 400

    new_category = Category(user_id=user_id, name=name)
    if post_data.get('description'):
        new_category.description = post_data.get('description')
    db.session.add(new_category)
    db.session.commit()
    response_object = {'status': 'success', 'data': [new_category.serialize()]}
    return jsonify(response_object), 201


@categories_blueprint.route('/categories/<int:cat_id>', methods=['PATCH'])
@authenticate
def update_user_category(user_id, cat_id):
    post_data = request.get_json()
    if not post_data:
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400

    category = Category.query.filter_by(id=cat_id).first()
    if not category or category.user_id != user_id:
        response_object = {
            'status': 'not found',
            'message': f'Category not found.',
        }
        return jsonify(response_object), 404
    name = post_data.get('name').lower()
    if (
        name
        and Category.query.filter(
            Category.user_id == user_id,
            Category.name == name,
            Category.id != cat_id,
        ).first()
    ):
        response_object = {
            'status': 'error',
            'message': f'A category named "{name}" already exists.',
        }
        return jsonify(response_object), 400
    if name:
        category.name = post_data.get('name')
    if post_data.get('description'):
        category.description = post_data.get('description')
    db.session.commit()
    response_object = {'status': 'success', 'data': [category.serialize()]}
    return jsonify(response_object), 200


@categories_blueprint.route('/categories/<int:cat_id>', methods=['DELETE'])
@authenticate
def delete_user_category(user_id, cat_id):
    category = Category.query.filter_by(id=cat_id).first()
    if not category or category.user_id != user_id:
        response_object = {
            'status': 'not found',
            'message': f'Category not found.',
        }
        return jsonify(response_object), 404
    if category.is_default:
        response_object = {
            'status': 'error',
            'message': 'Default category can not be deleted.',
        }
        return jsonify(response_object), 400
    if category.articles:
        # default category exists, no need to check it
        default_category = Category.query.filter_by(
            user_id=user_id, is_default=True
        ).first()
        for article in category.articles:
            article.category_id = default_category.id
            db.session.commit()
    db.session.delete(category)
    db.session.commit()
    response_object = {'status': 'no content'}
    return jsonify(response_object), 204
