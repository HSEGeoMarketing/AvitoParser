from selenium import webdriver
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import time
import csv

geolocator = Nominatim(user_agent="myGeocoder")
with open('commercial_premises.csv', "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(('Name', 'Price', 'Address', 'Latitude', 'Longitude', 'Link'))

i = 1

while i != 101:
    URL = f'https://www.avito.ru/sankt-peterburg/kommercheskaya_nedvizhimost/sdam-ASgBAgICAUSwCNRW?cd={i}'
    driver = webdriver.Chrome(
        executable_path="C:\\Users\\Пользователь\\Desktop\\project\\parsing\\parser\\ChromeWebDriver\\chromedriver.exe"
    )

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
            location = geolocator.geocode(address.text.strip())
            if location is not None:
                latitude = location.latitude
                longitude = location.longitude
            else:
                latitude = None
                longitude = None
            link = item.find('a', class_='link-link-MbQDP')
            link = link.get('href')
            link = 'https://www.avito.ru' + link
            with open('commercial_premises.csv', "a", encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (title.text.strip(), price.text.strip(), address.text.strip(), latitude,
                     longitude, link.strip()))

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
    i += 1
