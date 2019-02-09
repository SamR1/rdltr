from flask import Blueprint, jsonify, request

from .. import db
from ..users.utils import authenticate
from .model import Tag

tags_blueprint = Blueprint('tags', __name__)


@tags_blueprint.route('/tags', methods=['GET'])
@authenticate
def get_user_tags(user_id):
    tags = Tag.query.filter_by(id=user_id).all()
    response_object = {
        'status': 'success',
        'data': [tag.serialize() for tag in tags],
    }
    return jsonify(response_object), 200


@tags_blueprint.route('/tags', methods=['POST'])
@authenticate
def add_user_tag(user_id):
    post_data = request.get_json()
    if not post_data or post_data.get('name') is None:
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400

    name = post_data.get('name')
    tag = Tag.query.filter_by(user_id=user_id, name=name).first()
    if tag:
        response_object = {
            'status': 'error',
            'message': f'A tag named "{name}" already exists.',
        }
        return jsonify(response_object), 400

    new_tag = Tag(user_id=user_id, name=name)
    db.session.add(new_tag)
    db.session.commit()
    response_object = {'status': 'success', 'data': [new_tag.serialize()]}
    return jsonify(response_object), 201


@tags_blueprint.route('/tags/<int:tag_id>', methods=['PATCH'])
@authenticate
def update_user_tag(user_id, tag_id):
    post_data = request.get_json()
    if not post_data:
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400

    tag = Tag.query.filter_by(id=tag_id).first()
    if not tag or tag.user_id != user_id:
        response_object = {'status': 'not found', 'message': 'Tag no found.'}
        return jsonify(response_object), 404
    if post_data.get('name'):
        tag.name = post_data.get('name')
    db.session.commit()
    response_object = {'status': 'success', 'data': [tag.serialize()]}
    return jsonify(response_object), 200


@tags_blueprint.route('/tags/<int:tag_id>', methods=['DELETE'])
@authenticate
def delete_user_tag(user_id, tag_id):
    tag = Tag.query.filter_by(id=tag_id).first()
    if not tag or tag.user_id != user_id:
        response_object = {'status': 'not found', 'message': 'Tag no found.'}
        return jsonify(response_object), 404
    db.session.delete(tag)
    db.session.commit()
    response_object = {'status': 'no content'}
    return jsonify(response_object), 204
