import pytest
from unittest.mock import patch
from app.main import process_products


@pytest.fixture
def sample_product_data():
    return {
        "stock_code": "27356-01",
        "name": "Nakışlı elbise",
        "price": 5.24,
        "images":
        [
            "www.aday-butik-resim-sitesi/27356-turuncu-1.jpeg",
            "www.aday-butik-resim-sitesi/27356-turuncu-2.jpeg",
            "www.aday-butik-resim-sitesi/27356-turuncu-3.jpeg"
        ],
        "is_discounted": True,
        "color":
        [
            "Turuncu"
        ],
        "discounted_price": 2.24,
        "price_unit": "USD",
        "product_type": "Elbise",
        "quantity": 9,
        "sample_size": "S/36",
        "series": "1S-1M-2L-1XL",
        "status": "Active",
        "fabric": "%90 Polyester %10 Likra",
        "model_measurements": "Boy: 1.72, Göğüs: 86, Bel: 64, Kalça: 90",
        "product_measurements": "Boy: 42cm, Kol: 62cm"
    }


@patch('app.main.parse_xml')
@patch('app.main.MongoDBClient')
def test_process_products(mock_db_client, mock_parse_xml, sample_product_data):
    mock_parse_xml.return_value = [sample_product_data]
    db_client_instance = mock_db_client.return_value

    process_products('tests/files/lonca-sample.xml')

    mock_parse_xml.assert_called_once_with('tests/files/lonca-sample.xml')
    db_client_instance.insert_product.assert_called()
