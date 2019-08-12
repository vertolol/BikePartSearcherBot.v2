
from collections import deque

import requests
from bs4 import BeautifulSoup

URL = 'https://www.bike-discount.de/en/mountain-bike-parts/l-24'
url_site = 'https://www.bike-discount.de'
start_level = 2
end_level = 3
category_div = 'element-sidebar-warengruppe subwarengruppen uk-accordion-content'
class_ul = 'levell-{}'
categories = {}


def write_data_to_categories(li_category):
    name = li_category.a.text.strip().lower()
    value = li_category.a['href'].split('/')[-2]
    if name in categories:
        print(li_category.parent.parent.a.text)
    categories[name] = value


def get_link(li_cat):
    link = url_site + li_cat.a['href']
    return link


def get_category_ul(url, level):
    req = requests.get(url).text
    soup = BeautifulSoup(req, 'lxml')
    categories_bar = soup.find(class_=category_div)

    try:
        category_ul = categories_bar.find(class_=class_ul.format(level)).find_all('li')
    except:
        category_ul = []

    return category_ul


def fetch_data(url, level):
    list_urls = []
    ul_cat = get_category_ul(url, level)

    for li_cat in ul_cat:
        write_data_to_categories(li_cat)
        link = get_link(li_cat)

        if level != end_level:
            list_urls.append((link, level + 1))

    return list_urls


def depth_first_search(start_url, level):
    queue = deque()
    queue.append((start_url, level))

    while queue:
        url = queue.popleft()
        urls = fetch_data(url[0], url[1])
        queue.extend(urls)


depth_first_search(URL, start_level)


for cat in categories:
    print(cat, f'--{categories[cat]}--', sep=' ')
print(len(categories))
