import requests
from bs4 import BeautifulSoup
import sqlite3

d = []

try:
    sqlite_connection = sqlite3.connect('mashinki.db')
    cursor = sqlite_connection.cursor()
    # sqlite_create_table_query = '''CREATE TABLE car_search(
    #
    #                             carName text,
    #                             price text,
    #                             description text,
    #                             links text);'''

    print("База данных подключена к SQLite")
    # cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    print("Таблица SQLite создана")
except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)


class drom(object):

    def __init__(self):
        brand = 'audi'  # input('Введите марку автомобиля на английском ')
        model = ''  # input('Введите модель ')
        lowprice = 1444444  # int(input('Введите примерную стоимость '))
        minprice = lowprice - 50000
        maxprice = lowprice + 50000
        a = 1

        if lowprice < 50000:
            maxprice = 100000
        if model == '':
            model = 'all'
        for j in range(1, 3):
            # a+=a
            # указываем url и get параметры запроса
            url = f'https://auto.drom.ru/{brand}/{model}/page{j}/?minprice={minprice}&maxprice={maxprice}&?ph=1&pts=2&damaged=2&unsold=1&order=price'
            # указываем get параметр с помощью которого определяется номер страницы
            par = {'p': j}
            # записываем ответ сервера в переменную r
            r = requests.get(url, params=par)
            if r.status_code == 404:
                break
            # получаем объект  BeautifulSoup и записываем в переменную soup
            soup = BeautifulSoup(r.text, 'lxml')
            carName = soup.find_all('span', {'data-ftid': 'bull_title'})
            price = soup.find_all('span', {'data-ftid': 'bull_price'})
            description = soup.find_all('div', {'data-ftid': 'component_inline-bull-description'})
            links = soup.find_all('a', {'data-ftid': 'bulls-list_bull'})
            for i in range(0, len(carName)):
                nam = carName[i].text
                pr = price[i].text
                des = description[i].text
                li = links[i].get('href')
                cursor.execute("insert into car_search values (?,?,?,?)", (nam, pr, des, li))
                sqlite_connection.commit()



drom()
