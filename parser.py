from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import requests
import psycopg2

conn = psycopg2.connect('postgres://postgres:1111@localhost:5432/dbavito')
cur = conn.cursor()
cur.execute('''CREATE TABLE COMMERCIAL_PREMISES 
     (SQUARE DOUBLE PRECISION NOT NULL,
     PRICE INT NOT NULL,
     LATITUDE DOUBLE PRECISION NOT NULL,
     LONGITUDE DOUBLE PRECISION NOT NULL,
     LINK VARCHAR)
    ''')

product = input()
geolocator = Nominatim(user_agent="Tester")
url = "https://www.avito.ru/sankt-peterburg/nedvizhimost?q=" + product
request = requests.get(url)
bs = BeautifulSoup(request.text, "html.parser")
all_squares = bs.find_all("span", class_="desktop-3a1zuq")
all_addresses = bs.find_all("a", class_="geo-address-9QndR")
all_prices = bs.find_all("span", class_="price-price-38bRa")
all_links = bs.find_all("a",
                        class_="title-root-zZCwT body-title-drnL0 title-root_maxHeight-X6PsH text-text-LurtD text-size-s-BxGpL text-bold-SinUO")

for i in range(len(all_squares)):
    square = all_squares[i].text.replace(",", ".")
    price = all_prices[i].text.strip().replace(" ", "")
    location = geolocator.geocode(all_addresses[i].text)
    if location:
        lat = location.latitude
        long = location.longitude
    else:
        lat, long = None, None
    link = "https://www.avito.ru" + all_links[i]['href']
    cur.execute(
        "INSERT INTO COMMERCIAL_PREMISES (SQUARE, PRICE, LATITUDE, LONGITUDE, LINK) VALUES (%s, %s, %s, %s, %s)",
        (square, price, lat, long, link))

conn.commit()
conn.close()
