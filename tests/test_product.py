from unittest.mock import patch
import pytest
from models.product import Product
from datetime import datetime


@pytest.fixture
def mocked_datetime_now():
    with patch('models.product.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        yield mock_datetime.now.return_value


@pytest.fixture
def product():
    return Product(
        stock_code="2345-bej",
        name="nakışlı elbise",
        price=16.20,
        color=["Bej"],
        discounted_price=16.20,
        images=["www.aday-butik-resim-sitesi/27356-sarı.jpeg", "www.aday-butik-resim-sitesi/356-sarı.jpeg"],
        is_discounted=False,
        price_unit="USD",
        product_type="Elbise",
        quantity=3,
        sample_size="XL",
        series="2S-2M-2L",
        status="Active",
        fabric="%95 Pamuk % 5 Polyester",
        model_measurements="Boy: 1.79m, Göğüs: 88cm, Bel: 62cm, Kalça: 93cm",
        product_measurements="Boy: 1.65cm, Kilo: 56"
    )


def test_product_initialization(mocked_datetime_now, product):
    assert product.stock_code == "2345-bej"
    assert product.price == 16.20
    assert product.color == ["Bej"]
    assert product.discounted_price == 16.20
    assert product.images == ["www.aday-butik-resim-sitesi/27356-sarı.jpeg", "www.aday-butik-resim-sitesi/356-sarı.jpeg"]
    assert product.is_discounted is False
    assert product.price_unit == "USD"
    assert product.product_type == "Elbise"
    assert product.quantity == 3
    assert product.sample_size == "XL"
    assert product.series == "2S-2M-2L"
    assert product.status == "Active"
    assert product.fabric == "%95 Pamuk % 5 Polyester"
    assert product.model_measurements == "Boy: 1.79m, Göğüs: 88cm, Bel: 62cm, Kalça: 93cm"
    assert product.product_measurements == "Boy: 1.65cm, Kilo: 56"
    assert product.name == "Nakışlı elbise"
    assert product.created_at == mocked_datetime_now
    assert product.updated_at == mocked_datetime_now


def test_update_price(product, mocked_datetime_now):
    with patch('models.product.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 1, 1, 13, 0, 0)
        product.update_price(new_price=11.99)
        assert product.price == 11.99
        assert product.updated_at == mock_datetime.now.return_value
