from bcrypt import hashpw, gensalt
from flask import Blueprint
from flask_jwt_extended import create_access_token, jwt_required
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


@user_api.route('/login', methods=['POST'])
@use_kwargs(login_args)
def login_user(**kwargs):
    user = UserModel.get_by_username(kwargs['username'])
    if user and user.authenticate(kwargs['password']):
        return {"jwt_token": create_access_token(user.id)}
    return {"message": "Invalid username or password."}, 401


@user_api.route('/user/<string:username>', methods=['GET'])
def get_user(username):
    user = UserModel.get_by_username(username)
    if not user:
        return {"message": "User not found."}, 404
    return user.jsonify()


@user_api.route('/user/<string:username>', methods=['DELETE'])
@jwt_required()
def delete_user(username):
    user = UserModel.get_by_username(username)
    if not user:
        return {"message": "User not found."}, 404
    user.remove_from_db()
    return {"message": "Delete successful."}
