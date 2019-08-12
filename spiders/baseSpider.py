from abc import ABC, abstractmethod

import requests


class AbstractSpider(ABC):
    CATEGORY_CODES = None
    TEMPLATE_URL = None
    SIZE = 3

    def __init__(self, category, item_name):
        self.category_code = self.CATEGORY_CODES[category]['code']
        self.item_name = item_name
        if self.CATEGORY_CODES[category]['additional_string'] is not None:
            self.item_name = item_name + ' ' + self.CATEGORY_CODES[category]['additional_string']

    def get_html(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return  response.text

    def get_json(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            if response.headers['Content-Type'] == 'application/json':
                return response.json()

    @property
    def url(self):
        return self.TEMPLATE_URL.format(self.category_code, self.item_name.replace(' ', '%20'))

    @abstractmethod
    def get_list_items(self):
        pass

    @abstractmethod
    def scrape_data(self, item):
        pass

    @abstractmethod
    def price_to_float(self, price_string):
        pass

    def name_matches_result(self, cell):
        item_name_words = self.item_name.lower().split()
        result_name_words = list(cell.keys())[0].lower().split()
        if all(word in result_name_words for word in item_name_words):
            return cell
        return None

    def run(self):
        result_list = []
        for item in self.get_list_items():
            cell = self.scrape_data(item)
            if self.name_matches_result(cell):
                result_list.append(cell)

        result_list.sort(key=lambda x: list(x.values())[0]['price'])
        return result_list[:self.SIZE]
