from flask import Blueprint
from flask_jwt_extended import jwt_required
from webargs.flaskparser import use_kwargs

from Models.store import *

store_api = Blueprint('store_api', __name__)


@store_api.route('/stores', methods=['GET'])
def get_stores():
    return {"Stores": {store.name: store.jsonify() for store in StoreModel.get_all()}}


@store_api.route('/stores/<string:store_name>', methods=['GET'])
def get_store(store_name: str):
    store = StoreModel.get_by_name(store_name)
    if not store:
        return {"message": "Store not found."}, 404
    return store.jsonify()


@store_api.route('/stores', methods=['POST'])
@use_kwargs(store_args)
def post_store(**kwargs):
    if StoreModel.get_by_name(kwargs["name"]):
        return {"message": "A store with that name already exists."}, 400
    new_store = StoreModel(**kwargs)
    new_store.save_to_db()
    return new_store.jsonify(), 201


@store_api.route('/stores/<string:store_name>', methods=['DELETE'])
@jwt_required()
def delete_store(store_name: str):
    store = StoreModel.get_by_name(store_name)
    if not store:
        return {"message": "Store not found."}, 404
    for item in store.items:
        item.remove_from_db()
    store.remove_from_db()
    return {"message": "Delete successful."}
