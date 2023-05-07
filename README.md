# Парсер для Avito
Здесь представлен парсер для получения данных о аренде недвижимости c сайта Avito на Python.
## Просмотр объявлений и парсинг данных
Сначала происходит чтение данных о расположении магазинов и времени в пути от них до каждого из районов (market-coordinates, filled table, fixed_dist). Каждому из магазинов ставится в соответствие его уникальный ID. 
Сначала происходит просмотр страницы с помощью библиотеки Selenium.Дальше,с помощью библиотеки Beautiful Soup 4, мы считываем необходимые данные(название объявления, цена,площадь и адрес места,а также ссылка на объявление).
Все данные записываются в таблицу csv,где в дальнейшем проходит обработка данных.
## Обработка данных
Дальше необходимо преобразовать адрес в координаты.Для этого используется библиотека geopy.Благодаря ей и небольшой обработке данных можно преобразовать адрес в кооринаты:широту и долготу(latitude и longitude).
## Сохранение данных в базе данных
Дальше происходит подключение к базе данных и внесение данных в таблицу.Для этого используется PostgreSQL и Alchemy.

Ниже представлен пример работы парсера:
![Пример работы парсера](https://user-images.githubusercontent.com/112046185/236664722-9d9037b3-47e3-4759-8fc1-294c74c690b5.jpg)
