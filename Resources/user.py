from bcrypt import hashpw, gensalt
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from webargs.flaskparser import use_kwargs

from Models.user import *

user_api = Blueprint('user_api', __name__)


@user_api.route('/register', methods=['POST'])
@use_kwargs(user_args)
def register_user(**kwargs):
    if UserModel.get_by_username(kwargs['username']):
        return {"message": "Username already exists."}, 400
    user = UserModel(kwargs['username'], hashpw(kwargs['password'].encode(), gensalt()).decode('utf8'))
    user.save_to_db()
    return {"message": "User registration successful."}, 201


@user_api.route('/user/<string:username>', methods=['GET'])
def get_user(username):
    user = UserModel.get_by_username(username)
    if not user:
        return {"message": "User not found."}, 404
    return user.jsonify()


@user_api.route('/user/<string:username>', methods=['DELETE'])
@jwt_required(fresh=True)
def delete_user(username):
    claims = get_jwt()
    user = UserModel.get_by_username(username)
    if user and (user.id == get_jwt_identity() or claims['is_admin']):
        user.remove_from_db()
        return {"message": "Delete successful."}
    return {"message": "You may not delete other user accounts."}, 401
