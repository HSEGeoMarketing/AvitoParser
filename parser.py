import re
import requests
from bs4 import BeautifulSoup
import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(database="db_avito", user="postgres", password="1111", host="localhost", port="5432")
cursor = conn.cursor()

# Создание таблицы, если она еще не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS COMMERCIAL_PREMISES (
                        ID SERIAL PRIMARY KEY,
                        SQUARE DOUBLE PRECISION,
                        PRICE INT,
                        ADDRESS TEXT,
                        LATITUDE DOUBLE PRECISION,
                        LONGITUDE DOUBLE PRECISION,
                        LINK TEXT)''')
conn.commit()

# URL для поиска торговых площадей на Авито
url = "https://www.avito.ru/sankt-peterburg/kommercheskaya_nedvizhimost/prodam-ASgBAgICAUSSA8YQ"

# Загрузка страницы и парсинг HTML
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Поиск всех объявлений о продаже торговых площадей на странице
ads = soup.find_all('div', {'class': 'iva-item-root-Nj_hb'})

# Обход каждого объявления и извлечение данных
for ad in ads:
    link = ad.find('a', {'class': 'link-link-39EVK'})
    if link:
        href = link.get('href')
        url = f'https://www.avito.ru{href}'

        price = ad.find('span', {'class': 'price-price-32bra'}).text.strip().replace(' ', '')

        square = None
        square_regex = r'(\d+\.\d+) м²'
        square_match = re.search(square_regex, ad.text)
        if square_match:
            square = square_match.group(1)

        address = ad.find('span', {'class': 'geo-address-9QndR'})
        if address:
            address = address.text.strip()

        lat, lon = None, None
        map_link = ad.find('a', {'class': 'item__map'})
        if map_link:
            map_url = map_link.get('href')
            map_response = requests.get(map_url)
            map_soup = BeautifulSoup(map_response.content, 'html.parser')
            map_script = map_soup.find('script', {'type': 'application/json'})
            if map_script:
                map_data = map_script.text
                lat_lon_regex = r'"coordinates":\[(\d+\.\d+),(\d+\.\d+)\]'
                lat_lon_match = re.search(lat_lon_regex, map_data)
                if lat_lon_match:
                    lat = float(lat_lon_match.group(1))
                    lon = float(lat_lon_match.group(2))

        cursor.execute('''INSERT INTO COMMERCIAL_PREMISES 
                          (SQUARE, PRICE, ADDRESS, LATITUDE, LONGITUDE, LINK) 
                          VALUES (%s, %s, %s, %s, %s, %s)''', (square, price, address, lat, lon, url))
        conn.commit()

conn.close()
