from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, create_refresh_token
from webargs.flaskparser import use_kwargs

from Models.user import login_args, UserModel

session_api = Blueprint('session_api', __name__)


@session_api.route('/login', methods=['POST'])
@use_kwargs(login_args)
def login_user(**kwargs):
    user = UserModel.get_by_username(kwargs['username'])
    if user and user.authenticate(kwargs['password']):
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        return jsonify(access_token=access_token, refresh_token=refresh_token)
    return {"message": "Invalid username or password."}, 401


@session_api.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_jwt():
    identity = get_jwt_identity()
    new_token = create_access_token(identity)
    return jsonify(access_token=new_token)
