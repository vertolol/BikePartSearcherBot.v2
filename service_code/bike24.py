from collections import deque

import requests
from bs4 import BeautifulSoup

URL = 'https://www.bike24.com/mtb-trekking.html'
url_site = 'https://www.bike24.com/'
start_level = 3
end_level = 4
category_div = 'nav-main-item-lvl-1 item-active item-active-children'
class_ul = 'nav-main-list-lvl-{}'

categories = {}


def write_data_to_categories(li_cat):
    name = li_cat.find(class_='nav-main-link').text.strip().lower()
    value = li_cat.find(class_='nav-main-link')['data-nav'].split(',')[-1]
    categories[name] = value


def get_link(li_cat):
    try:
        link = url_site + li_cat.a['href']
    except:
        link = None
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


def depth_first_search(start_url, start_level):
    queue = deque()
    queue.append((start_url, start_level))

    while queue:
        url = queue.popleft()
        urls = fetch_data(url[0], url[1])
        queue.extend(urls)


depth_first_search(URL, start_level)
for cat in categories:
    print(cat, f'--{categories[cat]}--', sep=' ')
print(len(categories))
