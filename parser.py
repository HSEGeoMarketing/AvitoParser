import sqlite3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from math import ceil

URL_AVITO = f"https://www.avito.ru/sankt-peterburg/kommercheskaya_nedvizhimost"
EUR = 1


def avito_parser():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Задание user-agent
    ua = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
    options.add_argument(f"user-agent={ua}")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(15)
    driver.get(URL_AVITO)

    count = int(
        (
            driver.find_element(
                by=By.CSS_SELECTOR, value='span[data-marker="page-title/count"]'
            ).text
        ).replace(" ", "")
    )

    for _ in range(ceil(count / 50)):
        offer = []
        elems = driver.find_elements(
            by=By.CSS_SELECTOR, value='div[data-marker="item"]'
        )
        for elem in elems:
            try:
                avito_id = int(elem.get_attribute("id")[1:])
                url = elem.find_element(
                    by=By.CSS_SELECTOR, value='a[itemprop="url"]'
                ).get_attribute("href")
                item_address = elem.find_element(
                    by=By.CSS_SELECTOR, value='div[data-marker="item-address"]'
                ).text.split("\n")
                address = item_address[0]
                district = item_address[1]
                advert = elem.text.split("\n")
                price = round(int(advert[1][:-10].replace(" ", "")), 2)
                area = float(advert[0].split(", ")[1][:-3].replace(",", "."))
                parking = "Да" if "Парковка" in advert else "Нет"
                result = (area, price, address, parking, url)
                offer.append(result)

            except Exception as ex:
                print(ex)

        with sqlite3.connect("realty.db") as connection:
            cursor = connection.cursor()
            for data in offer:
                avito_id = data[0]
                cursor.execute(
                    """
                    SELECT avito_id FROM offers WHERE avito_id = (?)
                """,
                    (avito_id,),
                )
                result = cursor.fetchone()
                if result is None:
                    cursor.execute(
                        """
                        INSERT INTO offers
                        VALUES (NULL, ?, ?, ?, ?, ?, ?)
                    """,
                        data,
                    )
                    connection.commit()
                    print(f"Объявление {avito_id} добавлено в базу данных")
                else:
                    print(f"Объявление {avito_id} не добавлено в базу данных")
        driver.find_element(
            by=By.CSS_SELECTOR, value='span[data-marker="pagination-button/next"]'
        ).click()

    driver.quit()


if __name__ == "__main__":
    connection = sqlite3.connect("realty.db")
    cursor = connection.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS offers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    avito_id INTEGER UNIQUE NOT NULL,
                    area REAL NOT NULL,
                    price REAL NOT NULL,
                    address TEXT NOT NULL,
                    url TEXT NOT NULL
                    );
    """
    )
    connection.close()
    avito_parser()
