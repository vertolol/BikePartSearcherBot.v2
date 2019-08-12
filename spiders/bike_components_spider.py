from baseSpider import AbstractSpider
from category_codes.bike_components_category_codes import \
    bike_components_category_codes


class BikeComponentsSpider(AbstractSpider):
    CATEGORY_CODES = bike_components_category_codes
    TEMPLATE_URL =\
        r'https://www.bike-components.de/en/api/v1/catalog/RU/search/?filterCategoryPath={}&sort=price_asc&keywords={}'

    def __init__(self, category, item_name):
        super().__init__(category, item_name)

    def get_list_items(self):
        req = self.get_json()
        return req['products']

    def scrape_data(self, item):
        name = item['name']
        price_string = item['price']
        price = self.price_to_float(price_string)
        link = 'https://www.bike-components.de' + item['link']
        cell = {name: {'price': price, 'link': link}}
        return cell

    def price_to_float(self, price_string):
        return float(price_string.split()[-1][:-1].replace(',', ''))
