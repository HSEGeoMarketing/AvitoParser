import asyncio
import re
import aiohttp as aiohttp
from bs4 import BeautifulSoup
import asyncpg


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def parse_page(url, conn):
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
                            LINK TEXT)''')
    await conn.close()
    html = await fetch("https://www.avito.ru/sankt-peterburg/kommercheskaya_nedvizhimost/prodam-ASgBAgICAUSSA8YQ")
    soup = BeautifulSoup(html, 'html.parser')
    last_page = int(soup.find("span", {"class": "pagination-page"}).text)

    urls = [f"https://www.avito.ru/sankt-peterburg/kommercheskaya_nedvizhimost/prodam-ASgBAgICAUSSA8YQ?p={page}" for
            page in range(1, last_page + 1)]

    tasks = []
    for url in urls:
        tasks.append(asyncio.ensure_future(parse_page(url, conn)))
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
