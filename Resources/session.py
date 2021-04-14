import os
from datetime import timedelta
from urllib.parse import urlparse

from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, create_refresh_token, get_jwt
from redis import Redis
from webargs.flaskparser import use_kwargs

from Models.user import login_args, UserModel

ACCESS_TOKEN_TTL = timedelta(minutes=5)  # hours=1 in production

session_api = Blueprint('session_api', __name__)
# urlparse is necessary to avoid Unicode error on Heroku.
# see 'Connecting in Python', https://devcenter.heroku.com/articles/heroku-redis
redis_url = urlparse(os.environ.get('REDIS_TLS_URL'))
# Make sure redis is configured with AOF persistence in production!
jwt_redis_blocklist = Redis(host=redis_url.hostname, port=redis_url.port, username=redis_url.username,
                            password=redis_url.password, ssl=True, ssl_cert_reqs=None, decode_responses=True)


@session_api.route('/login', methods=['POST'])
@use_kwargs(login_args)
def login_user(**kwargs):
    user = UserModel.get_by_username(kwargs['username'])
    if user and user.authenticate(kwargs['password']):
        access_token = create_access_token(user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)
        return jsonify(access_token=access_token, refresh_token=refresh_token)
    return {"message": "Invalid username or password."}, 401


@session_api.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_jwt():
    identity = get_jwt_identity()
    new_token = create_access_token(identity)
    return jsonify(access_token=new_token)


@session_api.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_TOKEN_TTL)
    return {"message": "Logout successful."}, 205
