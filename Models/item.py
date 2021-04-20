from typing import Dict, List, Union

from webargs import fields

from Models.store import StoreModel
from db import db

ItemJson = Dict[str, Union[str, float, int]]


class ItemModel(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    store = db.relationship('StoreModel', back_populates='items')

    def __init__(self, name: str, price: float, store_id: int) -> None:
        self.name = name
        self.price = price
        self.store_id = store_id

    def jsonify(self) -> ItemJson:
        return {"name": self.name, "price": self.price, "store": self.store.name}

    @classmethod
    def get_all(cls) -> List["ItemModel"]:
        return cls.query.all()

    @classmethod
    def get_by_name(cls, name: str) -> "ItemModel":
        return cls.query.filter_by(name=name).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


item_args = {"name": fields.Str(required=True),
             "price": fields.Decimal(required=True, places=2, validate=lambda x: x >= 0),
             "store_id": fields.Integer(required=True, validate=lambda x: StoreModel.get_by_id(x) is not None)}
