from flask import Blueprint
from flask_jwt_extended import jwt_required
from webargs.flaskparser import use_kwargs

from Models.item import *

item_api = Blueprint('item_api', __name__)


@item_api.route('/items', methods=['GET'])
def get_items():
    return {"items": {item.name: item.jsonify() for item in ItemModel.get_all()}}


@item_api.route('/items/<string:item_name>', methods=['GET'])
def get_item(item_name: str):
    item = ItemModel.get_by_name(item_name)
    if item:
        return item.jsonify()
    return {"message": "Item not found."}, 404


@item_api.route('/items', methods=['POST'])
@use_kwargs(item_args)
def post_item(**kwargs):
    if ItemModel.get_by_name(kwargs['name']):
        return {"message": "Item already exists."}, 400
    new_item = ItemModel(**kwargs)
    new_item.save_to_db()
    return new_item.jsonify()


@item_api.route('/items', methods=['PUT'])
@use_kwargs(item_args)
def put_item(**kwargs):
    item = ItemModel.get_by_name(kwargs['name'])
    if not item:
        item = ItemModel(**kwargs)
        code = 201
    else:
        for k, v in kwargs.items():
            setattr(item, k, v)
        code = 200
    item.save_to_db()
    return item.jsonify(), code


@item_api.route('/items/<string:item_name>', methods=['DELETE'])
@jwt_required()
def delete_item(item_name: str):
    item = ItemModel.get_by_name(item_name)
    if not item:
        return {"message": "Item not found."}, 404
    item.remove_from_db()
    return {"message": "Delete successful."}
