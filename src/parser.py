import xml.etree.ElementTree as ET
from html.parser import HTMLParser


class ProductParser:
    def __init__(self, xml_string):
        self.root = ET.fromstring(xml_string)
        self.desc_parser = DescriptionParser()
        self.desc_parser.feed(self.root.find('./Description').text)

    def _name_changer(self, name):
        first_char = name[0] if name[0].isupper() else self._letter_upper(name[0])
        rest = name[1:].replace("I", "ı").replace("İ", "i").lower()
        return first_char + rest

    def _letter_upper(self, letter):
        change_list = {
            "i": "İ",
            "ı": "I"
        }
        return change_list.get(letter, letter)

    def parse(self):
        product = {}
        product['stock_code'] = self.root.attrib['ProductId']
        product['name'] = self._name_changer(self.root.attrib['Name'])
        product['price'] = float(self.root.find('.//ProductDetail[@Name="Price"]').attrib['Value'].replace(',', '.'))
        product['images'] = [img.attrib['Path'] for img in self.root.findall('./Images/Image')]
        product['color'] = None or [self.root.find('.//ProductDetail[@Name="Color"]').attrib['Value']]
        product['discounted_price'] = float(self.root.find('.//ProductDetail[@Name="DiscountedPrice"]').attrib['Value'].replace(',', '.'))
        product['is_discounted'] = product["price"] > product["discounted_price"]
        product['price_unit'] = "USD"
        product['product_type'] = self.root.find('.//ProductDetail[@Name="ProductType"]').attrib['Value']
        product['quantity'] = int(self.root.find('.//ProductDetail[@Name="Quantity"]').attrib['Value'])
        product['series'] = self.root.find('.//ProductDetail[@Name="Series"]').attrib['Value']
        product['sample_size'] = self.desc_parser.sample_size
        product['status'] = "Active"
        product['fabric'] = self.desc_parser.fabric
        product['model_measurements'] = self.desc_parser.model_measurements
        product['product_measurements'] = self.desc_parser.product_measurements
        return product


class DescriptionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.fabric = ""
        self.model_measurements = ""
        self.product_measurements = ""
        self.sample_size = ""
        self.recording = False
        self.current_data = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            self.recording = True
            self.current_data = ""

    def handle_endtag(self, tag):
        if tag == 'li':
            self.recording = False
            self.process_current_data()
            self.current_data = ""

    def handle_data(self, data):
        if self.recording:
            self.current_data += data

    def process_current_data(self):
        self.current_data = self.current_data.replace("\xa0", " ").replace('&nbsp;', ' ')
        if "Kumaş Bilgisi:" in self.current_data:
            self.fabric = self.current_data.split("Kumaş Bilgisi:")[1].strip()
        elif "Model Ölçüleri:" in self.current_data:
            self.model_measurements = self.current_data.split("Model Ölçüleri:")[1].strip()
        elif "Ürün Ölçüleri" in self.current_data:
            parts = self.current_data.split(":", 1)
            if len(parts) > 1:
                measurements = parts[1].strip().replace(' cm', 'cm,')
                measurements = measurements.replace("::", ":")
                measurements = measurements.replace("Boy:", "Boy: ").replace("Kol:", "Kol: ")
                self.product_measurements = ' '.join(measurements.split()).strip(",")
        elif "Modelin üzerindeki ürün" in self.current_data:
            size_info = self.current_data.split("bedendir.")[0].strip()
            self.sample_size = size_info.split()[-1]
