from app.mongo_client import MongoDBClient
from parser.parser import parse_multiple_products
from models.product import Product


def parse_xml(file_path):
    return parse_multiple_products(file_path)


def process_products(file_path):
    products = parse_xml(file_path)
    db_name = "lonca"
    collection_name = "loncaCollection"
    db_client = MongoDBClient(database_name=db_name, collection_name=collection_name)
    for prod in products:
        product = Product(**prod)
        db_client.insert_product(product)


if __name__ == '__main__':
    process_products('files/lonca-sample.xml')
