from datetime import datetime


class Product:
    def __init__(self, **kwargs) -> None:
        self.stock_code = kwargs["stock_code"]
        self.name = kwargs["name"].capitalize()
        self.images = kwargs["images"]
        self.price = kwargs["price"]
        self.color = kwargs["color"]
        self.discounted_price = kwargs["discounted_price"]
        self.is_discounted = kwargs["is_discounted"]
        self.price_unit = kwargs["price_unit"]
        self.product_type = kwargs["product_type"]
        self.quantity = kwargs["quantity"]
        self.sample_size = kwargs["sample_size"]
        self.series = kwargs["series"]
        self.status = kwargs["status"]
        self.fabric = kwargs["fabric"]
        self.model_measurements = kwargs["model_measurements"]
        self.product_measurements = kwargs["product_measurements"]
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update_price(self, new_price):
        self.price = new_price
        self._update_timestamp()

    def _update_timestamp(self):
        self.updated_at = datetime.now()
