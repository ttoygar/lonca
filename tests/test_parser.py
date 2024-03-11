import pytest
from parser.parser import ProductParser
import xml.etree.ElementTree as ET


def read_xml_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


@pytest.fixture
def multiple_products_xml():
    return read_xml_file('files/lonca-sample.xml')


@pytest.fixture
def product_xml():
    with open("tests/files/product.xml", "r", encoding="utf-8") as file:
        return file.read()


def test_parse_product(product_xml):
    expected = {
        'stock_code': "27356-01",
        'name': "Nakışlı elbise",
        'price': 5.24,
        'images': [
            "www.aday-butik-resim-sitesi/27356-turuncu-1.jpeg",
            "www.aday-butik-resim-sitesi/27356-turuncu-2.jpeg",
            "www.aday-butik-resim-sitesi/27356-turuncu-3.jpeg"
        ],
        'is_discounted': True,
        'color': ['Turuncu'],
        'discounted_price': 2.24,
        'price_unit': 'USD',
        'product_type': 'Elbise',
        'quantity': 9,
        'sample_size': 'S/36',
        'series': '1S-1M-2L-1XL',
        'status': 'Active',
        'fabric': '%90 Polyester %10 Likra',
        'model_measurements': "Boy: 1.72, Göğüs: 86, Bel: 64, Kalça: 90",
        'product_measurements': "Boy: 42cm, Kol: 62cm"
    }

    product_parser = ProductParser(product_xml)
    product = product_parser.parse()
    assert product == expected


def test_parse_product_starts_with_exotic_character(product_xml):
    exotic_character_xml = product_xml.replace("NAKIŞLI ELBİSE", "İ Harfli ELBİSE")
    product_parser = ProductParser(exotic_character_xml)
    product = product_parser.parse()

    assert product['name'] == "İ harfli elbise"


def test_parse_multiple_products(multiple_products_xml):
    root = ET.fromstring(multiple_products_xml)
    products = [ProductParser(ET.tostring(product).decode()) for product in root.findall('./Product')]

    assert len(products) > 0
    for product in products:
        parsed_data = product.parse()
        assert 'stock_code' in parsed_data
        assert 'name' in parsed_data
        assert 'price' in parsed_data
