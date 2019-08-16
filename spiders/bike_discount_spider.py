from bs4 import BeautifulSoup

from baseSpider import AbstractSpider
from category_codes.bike_discount_category_codes import \
    bike_discount_category_codes


class BikeDiscountSpider(AbstractSpider):
    CATEGORY_CODES = bike_discount_category_codes
    TEMPLATE_URL = r'https://www.bike-discount.de/en/{}/l-24/o-relevance?q={}'

    def __init__(self, category, item_name):
        super().__init__(category, item_name)

    def get_list_items(self):
        req = self.get_html()
        soup = BeautifulSoup(req, 'lxml')
        ul = soup.find(class_='warengruppe-detail-gallery uk-grid')
        list_items = ul.find_all(class_='uk-width-1-2 uk-width-medium-1-3')
        return list_items

    def scrape_data(self, item):
        name = ' '.join(item.find(class_='product-description').text.split())
        price_string = item.find(class_='price-value').text
        price = self.price_to_float(price_string)
        link = item.find(class_='productimage').a['href']
        img = item.find(class_='productimage').img['data-src']

        cell = {name: {'price': price,
                       'link': link,
                       'img': img}}
        return cell

    def price_to_float(self, price_string):
        return float(price_string.split()[0].replace('-', '0').replace(',', '.'))
