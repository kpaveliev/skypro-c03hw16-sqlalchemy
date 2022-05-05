import pytest


@pytest.fixture()
def user_keys():
    return {'id', 'first_name', 'last_name', 'age', 'email', 'role', 'phone'}


@pytest.fixture()
def order_keys():
    return {'id', 'name', 'description', 'start_date', 'end_date', 'address', 'price', 'customer_id', 'executor_id'}


@pytest.fixture()
def offer_keys():
    return {'id', 'order_id', 'executor_id'}
