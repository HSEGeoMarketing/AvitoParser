from selenium import webdriver
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import re
import time
import csv

geolocator = Nominatim(user_agent="myGeocoder")
with open('commercial_premises.csv', "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(('Name', 'Price', 'Square', 'Address', 'Latitude', 'Longitude', 'Link'))

# Specify the number of pages to parse
num_pages = 100

for i in range(1, num_pages + 1):
    URL = f'https://www.avito.ru/sankt-peterburg/kommercheskaya_nedvizhimost/sdam-ASgBAgICAUSwCNRW?cd={i}&p={i}'
    driver = webdriver.Chrome(
        executable_path="C:\\Users\\Пользователь\\Desktop\\project\\parsing\\parser\\ChromeWebDriver\\chromedriver.exe")

    try:
        driver.get(url=URL)
        main_page = driver.page_source
        time.sleep(1)
        main_source = BeautifulSoup(main_page, "html.parser")
        adt = main_source.find_all('div', class_='iva-item-content-rejJg')
        for item in adt:
            title = item.find('h3', class_='title-root-zZCwT')
            price = item.find('span', class_='price-text-_YGDY')
            address = item.find('div', class_='geo-address-fhHd0')
            location = None
            if address:
                address_text = address.text.strip()
                if 'пр-т' in address_text:
                    address_text = address_text.replace('пр-т', 'проспект')
                if 'Санкт-Петербург' not in address_text:
                    address_text = 'Санкт-Петербург, ' + address_text
                location = geolocator.geocode(address_text)

            regex = r"(\d+(\.\d+)?)(\s?)(м²|м2|кв\.м)"
            title_text = title.text.strip() if title else None
            match = re.search(regex, title_text) if title_text else None
            if match:
                square = match.group(1)
            else:
                square = None
            if location is not None:
                latitude = location.latitude
                longitude = location.longitude
            else:
                latitude = None
                longitude = None
            link = item.find('a', class_='link-link-MbQDP')
            link = link.get('href') if link else None
            link = 'https://www.avito.ru' + link if link else None
            price_text = price.text.replace('\xa0', '') if price else None

            with open('commercial_premises.csv', "a", encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (title.text.strip() if title else None, price_text, square,
                     address_text if address else None, latitude, longitude, link.strip() if link else None))

    except Exception as ex:
        print(ex)
    finally:
        driver.quit()
