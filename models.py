from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

db = SQLAlchemy()


class Loader:
    """Parent class for all models with general methods"""

    @classmethod
    def convert_date(cls, data: dict) -> dict:
        """ Convert date values of a dictionary into datetime.date format
        :param data: Source dictionary with some values in DD/MM/YYYY format
        :return: Dictionary with date fields converted to datetime.date
        """
        return {key: (datetime.strptime(value, '%m/%d/%Y')
                      if 'date' in key else value)
                for key, value in data.items()}


    @classmethod
    def create_instances(cls, path: str) -> list:
        """Create a list of class instances from a json file
        :param path: Path to a json file
        :return: Class instances list
        """
        # Load data from a json file
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return [cls(**cls.convert_date(el)) for el in data ]

    def update(self, updated_data: dict) -> None:
        """Update class object with data from a dictionary"""
        for key, value in updated_data.items():
            setattr(self, key, value)

    def instance_to_dict(self) -> dict:
        """Serialize the object as a dictionary"""
        return {key: value for key, value in vars(self).items() if key != '_sa_instance_state'}


class User(db.Model, Loader):
    """SQLAlchemy model for users"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    age = db.Column(db.Integer)
    email = db.Column(db.Text)
    role = db.Column(db.Text)
    phone = db.Column(db.Text)


class Order(db.Model, Loader):
    """SQLAlchemy model for orders"""
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.Text)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer = db.relationship('User', foreign_keys=[customer_id])
    executor = db.relationship('User', foreign_keys=[executor_id])
    offers = db.relationship('Offer')


class Offer(db.Model, Loader):
    """SQLAlchemy model for offers"""
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order = db.relationship('Order')
    executor = db.relationship('User')
