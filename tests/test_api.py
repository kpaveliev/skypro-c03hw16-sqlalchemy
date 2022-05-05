import tests.conftest
from app import app


class TestAPI:
    """Test 3 key GET end-points """

    def test_users(self, user_keys):
        """Check if users view returns json with correct keys"""
        response = app.test_client().get('/users')
        data = response.json
        assert isinstance(data, list), "API error (users): not list is returned"
        assert set(data[0].keys()) == user_keys, f"API error (users): keys aren't correct"

    def test_orders(self, order_keys):
        """Check if orders view returns json with correct keys"""
        response = app.test_client().get('/orders')
        data = response.json
        assert isinstance(data, list), "API error (orders): not list is returned"
        assert set(data[0].keys()) == order_keys, "API error (orders): keys aren't correct, "

    def test_offers(self, offer_keys):
        """Check if offers view returns json with correct keys"""
        response = app.test_client().get('/offers')
        data = response.json
        assert isinstance(data, list), "API error (offers): not list is returned"
        assert set(data[0].keys()) == offer_keys, "API error (offers): keys aren't correct"
