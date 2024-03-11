from pymongo import MongoClient


class MongoDBClient:
    def __init__(self, database_name, collection_name):
        self.client = MongoClient('mongodb://root:pass@mongo:27017/')
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def insert_product(self, product):
        product_dict = product.to_dict()
        if self.collection.find_one({"stock_code": product_dict["stock_code"]}) is None:
            return self.collection.insert_one(product_dict)
        else:
            return None

    def find_product(self, product_name):
        return self.collection.find_one({"name": product_name})
