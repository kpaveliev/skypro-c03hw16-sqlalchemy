from flask import Flask, redirect, jsonify, request, render_template
from models import db, User, Order, Offer

# Initiate app and load config
app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)


# Unnecessary views for convenience
@app.route("/")
def index():
    """Buttons to create/drop tables and links to key api pages"""
    return render_template('index.html')


@app.route("/create_all")
def create_all():
    """Create database, tables, populate tables with data from json files"""
    db.create_all()
    with db.session.begin():
        users = User.create_instances(app.config.get('USERS'))
        orders = Order.create_instances(app.config.get('ORDERS'))
        offers = Offer.create_instances(app.config.get('OFFERS'))
        db.session.add_all(users)
        db.session.add_all(orders)
        db.session.add_all(offers)
    message = 'Tables successfully created and populated'
    return render_template('result.html', message=message)


@app.route("/drop_all")
def drop_all():
    """Drop all tables in the database"""
    db.drop_all()
    message = 'Tables successfully dropped'
    return render_template('result.html', message=message)


# Required API views
@app.route("/users", methods=['GET', 'POST'])
def users_all():
    """
    GET - display all users in the database
    POST - add new user to the database from a json
    """
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
    """
    For user with specified id
    GET - display user
    PUT - update user with the information from a json
    DELETE - delete user
    """
    if request.method == 'PUT':
        data = request.json
        with db.session.begin():
            user = User.query.filter(User.id == idx).one()
            user.update(data)
            return jsonify(user.instance_to_dict())

    elif request.method == 'DELETE':
        with db.session.begin():
            User.query.filter(User.id == idx).delete()
        return redirect('/users', 302)

    else:
        user = User.query.filter(User.id == idx).one()
        return jsonify(user.instance_to_dict())


@app.route("/orders", methods=['GET', 'POST'])
def orders_all():
    """
    GET - display all orders in the database
    POST - add new order to the database from a json
    """
    if request.method == 'POST':
        with db.session.begin():
            data = request.json
            data_changed = Order.convert_date(data)
            order = Order(**data_changed)
            db.session.add(order)
            return jsonify(order.instance_to_dict())
    else:
        orders = Order.query.all()
        orders_json = [order.instance_to_dict() for order in orders]
        return jsonify(orders_json)


@app.route("/orders/<int:idx>", methods=['GET', 'PUT', 'DELETE'])
def order_by_id(idx):
    """
    For order with specified id
    GET - display order
    PUT - update order with the information from a json
    DELETE - delete order
    """
    if request.method == 'PUT':
        data = request.json
        data_changed = Order.convert_date(data)
        with db.session.begin():
            order = Order.query.filter(Order.id == idx).one()
            order.update(data_changed)
            return jsonify(order.instance_to_dict())

    elif request.method == 'DELETE':
        with db.session.begin():
            Order.query.filter(Order.id == idx).delete()
        return redirect('/orders', 302)

    else:
        Customer = db.aliased(User)
        Executor = db.aliased(User)
        query_result = db.session\
            .query(Order.id,
                   Order.description,
                   Executor.last_name.label('executor_name'),
                   Customer.last_name.label('customer_name'))\
            .join(Executor, Order.executor_id == Executor.id)\
            .join(Customer, Order.customer_id == Customer.id)\
            .filter(Order.id == idx).one()
        return jsonify(query_result._asdict())


@app.route("/offers", methods=['GET', 'POST'])
def offers_all():
    """
    GET - display all offers in the database
    POST - add new offer to the database from a json
    """
    if request.method == 'POST':
        with db.session.begin():
            offer = Offer(**request.json)
            db.session.add(offer)
            return jsonify(offer.instance_to_dict())
    else:
        offers = Offer.query.all()
        offers_json = [offer.instance_to_dict() for offer in offers]
        return jsonify(offers_json)


@app.route("/offers/<int:idx>", methods=['GET', 'PUT', 'DELETE'])
def offer_by_id(idx):
    """
    For offer with specified id
    GET - display offer
    PUT - update offer with the information from a json (date values only in MM/DD/YYYY format)
    DELETE - delete offer
    """
    if request.method == 'PUT':
        data = request.json
        with db.session.begin():
            offer = Offer.query.filter(Offer.id == idx).one()
            offer.update(data)
            return jsonify(offer.instance_to_dict())

    elif request.method == 'DELETE':
        with db.session.begin():
            Offer.query.filter(Order.id == idx).delete()
        return redirect('/offers', 302)

    else:
        offer = Offer.query.filter(Offer.id == idx).one()
        return jsonify(offer.instance_to_dict())


if __name__ == '__main__':
    app.run()
