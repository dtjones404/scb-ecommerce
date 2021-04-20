from typing import Dict, Union

from bcrypt import checkpw
from webargs import fields, validate

from db import db

UserJson = Dict[str, Union[str, int]]


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def jsonify(self) -> UserJson:
        return {"id": self.id, "username": self.username}

    @classmethod
    def get_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def authenticate(self, password: str) -> bool:
        return checkpw(password.encode('utf8'), self.password.encode('utf8'))


pw_regex = '^(?=\S{8,64}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])'
user_args = {"username": fields.Str(required=True, validate=validate.Length(min=4, max=64)),
             "password": fields.Str(required=True, validate=validate.Regexp(pw_regex))}

login_args = {"username": fields.String(required=True),
              "password": fields.String(required=True)}
