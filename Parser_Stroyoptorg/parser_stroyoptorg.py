import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cards.csv'
HOST = 'https://new.optorg.ru'
URL =  'https://new.optorg.ru/catalog/avtomobilnye_tovary_shiny/shiny_i_komplektuyushchie/legkovye_shiny/'
HEADERS= {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

def get_html(url, params=''):
        r = requests.get(url, headers= HEADERS, params=params)
        return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='list_item')
    cards = []
    
    for item in items:
        cards.append(
            {
                'title': item.find('div', class_="item-title").find('a').find('span').text,
                'link_product': HOST + item.find('div', class_="item-title").find('a').get('href'),
                'price': item.find('div', class_="price_value_block").find('span', class_="price_value").text.replace('\xa0', ''),
            }
        )
    return cards   
#html = get_html(URL)
#get_content(html.text)
#print(get_content(html.text))

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название шины', 'Ссылка', 'Стоимость'])
        for item in items:
             writer.writerow([item['title'], item['link_product'], item['price']])


def parser():
    PAGENATION = input('Укажите количество страниц для парсинга: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    cards = []
    if html.status_code == 200:
        for page in range(1, PAGENATION):
            print(f'Парсим страницу: {page}')
            html = get_html(URL, params={'PAGEN_1': page})
            cards.extend(get_content(html.text))
            save_doc(cards, CSV)
        print('Парсинг закончили!')
        print(cards)
    else:
        print('error') 

parser()
