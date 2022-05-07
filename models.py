from flask_sqlalchemy import SQLAlchemy
import json
import datetime

db = SQLAlchemy()


class Loader:
    """Parent class for all models with general methods"""

    @classmethod
    def convert_date(cls, data: dict) -> dict:
        """ Convert date values of a dictionary into datetime.date format

        :param data: Source dictionary with some values in DD/MM/YYYY format
        :return: Dictionary with date fields converted to datetime.date
        """
        data_changed = {}
        for key, data in data.items():
            if 'date' in key:
                month, day, year = data.split('/')
                date_new = datetime.date(int(year), int(month), int(day))
                data_changed[key] = date_new
            else:
                data_changed[key] = data
        return data_changed

    @classmethod
    def create_instances(cls, path: str) -> list:
        """Create a list of class instances from a json file

        :param path: Path to a json file
        :return: Class instances list
        """
        # Load data from a json file
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # Create and append class objects list
        objects_list = []
        for item in data:
            # Change date format to datetime.date
            item_changed = cls.convert_date(item)
            objects_list.append(cls(**item_changed))
        return objects_list

    def update(self, updated_data: dict) -> None:
        """Update class object with data from a dictionary"""
        for key, value in updated_data.items():
            setattr(self, key, value)

    @classmethod
    def make_dict(cls, list_):
        # dict = {}
        # for attr in dir(self):
        #     dict[attr] = getattr(self, attr)
        # return dict
        return {
            "order_id": list_[0],
            "order_description": list_[1],
            "executor_name": list_[2],
            "customer_name": list_[3]
        }


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

    def instance_to_dict(self) -> dict:
        """Serialize object as a dictionary"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


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

    def instance_to_dict(self) -> dict:
        """Serialize object as a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model, Loader):
    """SQLAlchemy model for offers"""
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order = db.relationship('Order')
    executor = db.relationship('User')

    def instance_to_dict(self) -> dict:
        """Serialize object as a dictionary"""
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }
