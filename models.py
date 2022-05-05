from flask_sqlalchemy import SQLAlchemy
import json
import datetime
db = SQLAlchemy()


class Loader:

    @classmethod
    def create_instances(cls, path: str) -> list:
        """ Create list of class objects from json

        :param path: Path to json file
        :return: List of the Model_name objects
        """
        # Load data from the json
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Create list of the objects and append it with the Model_name objects
        objects_list = []
        for item in data:

            item_changed = {}
            for key, data in item.items():
                # Replace MM/DD/YYYY fields with datetime.date objects
                if 'date' in key:
                    month, day, year = data.split('/')
                    date_new = datetime.date(int(year), int(month), int(day))
                    item_changed[key] = date_new
                else:
                    item_changed[key] = data
            objects_list.append(cls(**item_changed))
            # objects_list.append(cls(**item))

        return objects_list

    def update(self, new_data):
        for key, value in new_data.items():
            setattr(self, key, value)


class User(db.Model, Loader):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    age = db.Column(db.Integer)
    email = db.Column(db.Text)
    role = db.Column(db.Text)
    phone = db.Column(db.Text)

    def instance_to_dict(self) -> dict:
        """Serialize object as dictionary"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }

    def change_instance(self, data: dict):
        self.id = data.get('id')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.age = data.get('age')
        self.email = data.get('email')
        self.role = data.get('role')
        self.phone = data.get('phone')


class Order(db.Model, Loader):
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

    def instance_to_dict(self):
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

    def change_instance(self, data: dict):
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.start_date = data.get('start_date')
        self.end_date = data.get('end_date')
        self.address = data.get('address')
        self.price = data.get('price')
        self.customer_id = data.get('customer_id')
        self.executor_id = data.get('executor_id')


class Offer(db.Model, Loader):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    order = db.relationship('Order')
    executor = db.relationship('User')

    def instance_to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }

if __name__ == '__main__':
    db.create_all()
