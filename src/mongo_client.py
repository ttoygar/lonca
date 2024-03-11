from pymongo import MongoClient


class MongoDBClient:
    def __init__(self, database_name, collection_name):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def insert_product(self, product):
        if self.collection.find_one({"name": product["name"]}) is None:
            return self.collection.insert_one(product)
        else:
            return None

    def find_product(self, product_name):
        return self.collection.find_one({"name": product_name})
