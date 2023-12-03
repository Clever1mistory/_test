import requests
from bs4 import BeautifulSoup


def get_open_graph_data(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Проверка наличия open graph разметки
    og_data = {
        'title': '',
        'description': '',
        'image': ''
    }
    og_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
    if og_tags:
        for tag in og_tags:
            if tag.attrs.get('property') == 'og:title':
                og_data['title'] = tag.attrs.get('content')
            elif tag.attrs.get('property') == 'og:description':
                og_data['description'] = tag.attrs.get('content')
            elif tag.attrs.get('property') == 'og:image':
                og_data['image'] = tag.attrs.get('content')

    # Если open graph разметки нет, получаем данные из тегов title и meta description
    if not og_data['title']:
        title_tag = soup.find('title')
        if title_tag:
            og_data['title'] = title_tag.string

    if not og_data['description']:
        meta_description_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_description_tag:
            og_data['description'] = meta_description_tag.attrs.get('content')

    return og_data
