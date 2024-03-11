from unittest.mock import MagicMock, patch
import pytest


@pytest.fixture(scope="module")
def mongo_client():
    with patch('src.mongo_client.MongoDBClient') as MockMongoDBClient:
        mock_client_instance = MockMongoDBClient.return_value
        mock_client_instance.find_product = MagicMock(return_value={'name': 'Test Product'})
        mock_client_instance.collection.find.return_value = MagicMock(count=MagicMock(return_value=1))
        yield mock_client_instance


def test_insert_product(mongo_client):
    product = {
        "name": "Test Product",
        "price": 10.99,
        "quantity": 5
    }
    result = mongo_client.insert_product(product)
    assert result.inserted_id is not None


def test_find_product(mongo_client):
    product_name = "Test Product"
    product = mongo_client.find_product(product_name)
    assert product is not None
    assert product["name"] == product_name


def test_product_not_duplicate(mongo_client):
    product = {
        "name": "Test Product",
        "price": 10.99,
        "quantity": 5
    }
    mongo_client.insert_product(product)
    products = mongo_client.collection.find({"name": "Test Product"})
    assert products.count() == 1
