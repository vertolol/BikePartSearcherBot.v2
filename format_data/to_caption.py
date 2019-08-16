

def get_caption(results, index):
    text =''
    for ind, item in enumerate(results, index):
        name = list(item.keys())[0]
        price = item[name]['price']
        url = item[name]['link']
        text += f'{ind}. <b>{price}€</b> {name} \n<a href="{url}">{url[:35]}...</a>\n'

    return text