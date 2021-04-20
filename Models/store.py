from typing import Dict, List, Union

from webargs import fields

from Models.item import ItemJson
from db import db

storeJson = Dict[str, Union[int, str, Dict[str, ItemJson]]]


class StoreModel(db.Model):
    __tablename__ = 'store'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    items = db.relationship('ItemModel', back_populates='store')

    def __init__(self, name: str) -> None:
        self.name = name

    @classmethod
    def get_all(cls) -> List["StoreModel"]:
        return cls.query.all()

    @classmethod
    def get_by_name(cls, name: str) -> "StoreModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_by_id(cls, id: int) -> "StoreModel":
        return cls.query.filter_by(id=id).first()

    def jsonify(self) -> Dict:
        return {"id": self.id, "name": self.name, "items": {item.name: item.price for item in self.items}}

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


store_args = {"name": fields.Str(required=True)}
