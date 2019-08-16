from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
from typing import TypeVar, List

item_type = TypeVar('item_type', dict, BeautifulSoup)


class AbstractSpider(ABC):
    """Базовый класс для извлечеия данных с сайта
    CATEGORY_CODES: словарь с кодами категорий
    TEMPLATE_URL: шаблон url в который подставляются код категрии и название детали
    SIZE: количство деталей по которым нужно вернуть информацию
    """
    CATEGORY_CODES = None
    TEMPLATE_URL = None
    SIZE = 3

    def __init__(self, category: str, item_name: str):
        """
        :param category: категория в которой будет поиск детали
        :param item_name: название детали
        """
        self.category_code = self.CATEGORY_CODES[category]['code']
        self.item_name = item_name
        if self.CATEGORY_CODES[category]['additional_string'] is not None:
            self.item_name = item_name + ' ' + self.CATEGORY_CODES[category]['additional_string']

    def get_html(self) -> str:
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.text

    def get_json(self) -> dict:
        response = requests.get(self.url)
        if response.status_code == 200:
            if response.headers['Content-Type'] == 'application/json':
                return response.json()

    @property
    def url(self) -> str:
        return self.TEMPLATE_URL.format(self.category_code, self.item_name.replace(' ', '+'))

    @abstractmethod
    def get_list_items(self) -> List[item_type]:
        """
        Находит и извлекает список данных о деталях со страницы,
        по адресу self.url, с помощью метода get_json или get_html
        :return: список с данными о деталях
        """
        pass

    @abstractmethod
    def scrape_data(self, item: item_type) -> dict:
        """
        Извлекает информацию о конкретной детали
        :param item: контейнер с описанием детали
        :return: словарь с информацией о детали в формате:
        {name: {'price': price,
                'link': link,
                'img': img}}
        """
        pass

    @abstractmethod
    def price_to_float(self, price_string: str) -> float:
        pass

    def name_matches_result(self, cell: dict) -> dict or None:
        """
        Проверяет вхождение слов из названия детали для которой производится поиск,
        с названием детали которую нашли на сайте.
        :param cell: словарь с данными детали
        :return: словарь если проверка прошла успешно,
        None если проверка не прошла
        """
        item_name_words = self.item_name.lower().split()
        result_name_words = list(cell.keys())[0].lower().split()
        if all(word in result_name_words for word in item_name_words):
            return cell

    def run(self) -> list:
        result_list = []
        for item in self.get_list_items():
            cell = self.scrape_data(item)
            if self.name_matches_result(cell):
                result_list.append(cell)

        result_list.sort(key=lambda x: list(x.values())[0]['price'])
        return result_list[:self.SIZE]
