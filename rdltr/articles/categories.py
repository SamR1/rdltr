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
def add_user_categories(user_id):
    post_data = request.get_json()
    if not post_data or post_data.get('name') is None:
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400

    name = post_data.get('name')
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
