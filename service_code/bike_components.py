from collections import deque

import requests

URL = 'https://www.bike-components.de/en/api/v1/catalog/RU/search/?filterCategoryPath=60000000'
url_site = 'https://www.bike-components.de/en/api/v1/catalog/RU/category/{}/'
start_level = 1
end_level = 3

categories = {}


def get_link(li_cat):
    link = url_site.format(li_cat["value"])
    return link


def write_data_to_categories(li_cat):
    name = li_cat["label"].lower()
    value = li_cat["value"]
    categories[name] = value


def get_category_ul(url):
    data = requests.get(url).json()
    try:
        categories_container = data['filters'][1]['items']
    except:
        categories_container = data['filters'][0]['items']
    return categories_container


def fetch_data(url, level):
    list_urls = []
    ul_cat = get_category_ul(url)

    for li_cat in ul_cat:
        if li_cat["level"] != level:
            continue
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
