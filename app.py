import os

from flask import Flask
from flask_jwt_extended import JWTManager

from Resources.item import item_api
from Resources.session import session_api
from Resources.store import store_api
from Resources.user import user_api
from db import db
from security import *

app = Flask(__name__)
# replace method is a necessary compatibility workaround. See commit 'd4af'.
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    'DATABASE_URL', "sqlite:///data.db").replace('postgres://', 'postgresql://')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["JWT_SECRET_KEY"] = get_secret()
jwt = JWTManager(app)
db.init_app(app)

app.register_blueprint(item_api)
app.register_blueprint(store_api)
app.register_blueprint(user_api)
app.register_blueprint(session_api)


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    return {'is_admin': True if identity == 1 else False}


@app.errorhandler(422)
@app.errorhandler(400)
def handle_errors(err):
    messages = err.data.get("messages", ["Invalid request"])
    headers = err.data.get("headers", None)
    return {"errors": messages}, err.code, headers if headers else None


if __name__ == '__main__':
    app.run(debug=True)
