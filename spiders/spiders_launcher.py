from bike24_spider import Bike24Spider
from bike_components_spider import BikeComponentsSpider
from bike_discount_spider import BikeDiscountSpider

spiders = {
    'bike_24': Bike24Spider,
    'bike_components': BikeComponentsSpider,
    'bike_discount': BikeDiscountSpider,
}


def run_spiders(stores: list, category: str, item_name: str) -> str:
    """
    Запускает пауков из списка stores
    :param stores: список магазинов в которых будет производится поиск
    :param category: название категории
    :param item_name: название детали
    :return: HTML с результатами поиска
    """
    result_list = []
    for store in stores:
        res = spiders[store](category, item_name).run()
        result_list.extend(res)

    result_list.sort(key=lambda x: list(x.values())[0]['price'])
    return repr_in_html(result_list)


def repr_in_html(result_list: list) -> str:
    """
    :return: список результатов в HTML
    """
    text = ''
    for ind, item in enumerate(result_list, 1):
        name = list(item.keys())[0]
        price = item[name]['price']
        url = item[name]['link']
        text += f'{ind}. <b>{price}€</b> {name} \n<a href="{url}">{url[:35]}...</a>\n'

    return text
