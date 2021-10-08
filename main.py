import requests
from bs4 import BeautifulSoup

d = []

brand = input('Введите марку автомобиля на английском ')
model = input('Введите модель ')

for j in range(1):
    # указываем url и get параметры запроса
    url = f'https://auto.drom.ru/{brand}/{model}/?ph=1&pts=2&damaged=2&unsold=1'
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
        print(i, carName[i].text + ' цена ' + price[i].text + 'Р.' + description[i].text + links[i].get('href'))



# <span class="css-bhd4b0 e162wx9x0"><span data-ftid="bull_price">3 320 000<!-- --> </span>₽</span>
# <span data-ftid="bull_title">Audi Q5, 2018</span>
# <a class="css-1psewqh ewrty961" data-ftid="bulls-list_bull" href="https://novosibirsk.drom.ru/audi/q5/43793354.html">