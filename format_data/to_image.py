from PIL import Image
import requests
import os

url1 = r'https://cdn.bike24.net/i/p/1/2/106221_00_c.jpg'
url2 = r'https://cdn.bike-discount.de/media/org/orgb_S/orgid_65/thumbs/119275_704929.jpg'
# url3 = r'https://cdn.bike-discount.de/media/org/orgb_S/orgid_65/thumbs/211157_1440713.jpg'

urls = [url1, url2]
dir_for_images = os.path.join(os.getcwd(), 'format_data\\temporary_file\\')


def get_img_file(url: str) -> str:
    image_name = url.split('/')[-1]
    image_file = dir_for_images + image_name

    with open(image_file, 'wb') as img_file:
        img_data = requests.get(url).content
        img_file.write(img_data)

    return image_file


def paste_number(image_file, number: int, x_num_size=17, y_num_size=23) -> str:
    num_file_template = os.path.join(os.getcwd(), 'format_data\\nums\\{}.jpg')
    y_size = image_file.size[1]
    num_file = num_file_template.format(number)
    num_image = Image.open(num_file).resize((x_num_size, y_num_size))
    ''' вставить номер в нижний левый угол '''
    image_file.paste(num_image, (0, y_size - y_num_size))

    return image_file


def get_urls(results):
    urls = []

    for ind, item in enumerate(results):
        name = list(item.keys())[0]
        urls.append(item[name]['img'])
    return urls


def get_merge_image(results: list, index) -> str:
    x_size, y_size = 180, 128

    merge_image = Image.new('RGB', (x_size * len(results), y_size))
    merge_image_file = dir_for_images + 'merge_image.jpg'

    urls = get_urls(results)

    for number, url in enumerate(urls):
        img_file = get_img_file(url)
        for_paste = Image.open(img_file).resize((x_size, y_size))
        for_paste_numbered = paste_number(for_paste, number + index)
        merge_image.paste(for_paste_numbered, (x_size * number, 0))

    merge_image.save(merge_image_file)

    return merge_image_file

