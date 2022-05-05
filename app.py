from flask import Flask, redirect, jsonify, request
from models import db, User, Order, Offer
import json

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

@app.route("/")
def index():
    return f'<h1>Заглушка</h1>'


@app.route("/create_all")
def create_all():
    db.create_all()
    with db.session.begin():
        # users = assign_model(User, app.config.get('USERS'))
        # orders = assign_model(Order, app.config.get('ORDERS'))
        # offers = assign_model(Offer, app.config.get('OFFERS'))
        users = User.create_instances(app.config.get('USERS'))
        orders = Order.create_instances(app.config.get('ORDERS'))
        offers = Offer.create_instances(app.config.get('OFFERS'))
        db.session.add_all(users)
        db.session.add_all(orders)
        db.session.add_all(offers)
    return f'<h1>Данные добавлены</h1>'


@app.route("/users", methods=['GET', 'POST'])
def users_all():
    if request.method == 'POST':
        with db.session.begin():
            user = User(**request.json)
            db.session.add(user)
        return jsonify(user.instance_to_dict())
    else:
        users = User.query.all()
        users_json = [user.instance_to_dict() for user in users]
        return jsonify(users_json)


@app.route("/users/<int:idx>", methods=['GET', 'PUT', 'DELETE'])
def user_by_id(idx):
    # Get instance
    # user = User.query.filter(User.id == idx).one()

    if request.method == 'PUT':
        data = request.json
        with db.session.begin():
            # user.change_instance(data)
            user = User.query.filter(User.id == idx).one()
            user.update(data)
        return jsonify(user.instance_to_dict())
        # return redirect('/users', 302)

    elif request.method == 'DELETE':
        with db.session.begin():
            user = User.query.filter(User.id == idx).one()
            user.delete()
        return redirect('/users', 302)

    else:
        user = User.query.filter(User.id == idx).one()
        return jsonify(user.instance_to_dict())


@app.route("/orders")
def orders_all():
    orders = Order.query.all()
    orders_json = [order.instance_to_dict() for order in orders]
    return jsonify(orders_json)


@app.route("/orders/<int:idx>")
def order_by_id(idx):
    order = Order.query.filter(Order.id == idx).one()
    return jsonify(order.instance_to_dict())


@app.route("/offers")
def offers_all():
    offers = Offer.query.all()
    offers_json = [offer.instance_to_dict() for offer in offers]
    return jsonify(offers_json)


@app.route("/offers/<int:idx>")
def offer_by_id(idx):
    offer = Offer.query.filter(Offer.id == idx).one()
    return jsonify(offer.instance_to_dict())


if __name__ == '__main__':
    app.run()
