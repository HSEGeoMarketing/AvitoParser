import asyncio
import re
import aiohttp as aiohttp
from bs4 import BeautifulSoup
import asyncpg
import random
import time


async def fetch(url, headers=None, proxy=None):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, proxy=proxy) as response:
            return await response.text()


async def parse_page(url, conn):
    # Имитация естественного поведения
    delay = random.uniform(1, 3)  # Случайная задержка от 1 до 3 секунд
    await asyncio.sleep(delay)

    html = await fetch(url)
    soup = BeautifulSoup(html, 'html.parser')
    ads = soup.find_all('div', {'class': 'iva-item-root-Nj_hb'})
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
                map_html = await fetch(map_url)
                map_soup = BeautifulSoup(map_html, 'html.parser')
                map_script = map_soup.find('script', {'type': 'application/json'})
                if map_script:
                    map_data = map_script.text
                    lat_lon_regex = r'"coordinates":\[(\d+\.\d+),(\d+\.\d+)\]'
                    lat_lon_match = re.search(lat_lon_regex, map_data)
                    if lat_lon_match:
                        lat = float(lat_lon_match.group(1))
                        lon = float(lat_lon_match.group(2))
            await conn.execute('''INSERT INTO COMMERCIAL_PREMISES 
                                  (SQUARE, PRICE, ADDRESS, LATITUDE, LONGITUDE, LINK) 
                                  VALUES ($1, $2, $3, $4, $5, $6)''', (square, price, address, lat, lon, url))


async def main():
    conn = await asyncpg.connect(database="db_avito", user="postgres", password="1111", host="localhost", port="5432")
    await conn.execute('''CREATE TABLE IF NOT EXISTS COMMERCIAL_PREMISES (
                            ID SERIAL PRIMARY KEY,
                            SQUARE DOUBLE PRECISION,
                            PRICE INT,
                            ADDRESS TEXT,
                            LATITUDE DOUBLE PRECISION,
                            LONGITUDE DOUBLE PRECISION,
LINK TEXT);''')
    urls = ['https://www.avito.ru/moskva/kommercheskaya_nedvizhimost/prodam',
            'https://www.avito.ru/moskva/kommercheskaya_nedvizhimost/prodam?p=2',
            'https://www.avito.ru/moskva/kommercheskaya_nedvizhimost/prodam?p=3']

    tasks = []
    for url in urls:
        tasks.append(parse_page(url, conn))

    await asyncio.gather(*tasks)

    await conn.close()
