from tkinter import *
from tkinter import ttk
from tkinter.tix import *
import sqlite3
import requests
from bs4 import BeautifulSoup
import webbrowser

# соединение с базой данных
connection = sqlite3.connect(':memory:')
cursor = connection.cursor()
sqlite_create_table_query = '''CREATE TABLE car_search(

                                carName text,
                                price text,
                                description text,
                                links text);'''
cursor.execute(sqlite_create_table_query)
connection.commit()
cursor.execute("SELECT * FROM car_search")


class drom(object):

    def __init__(self):
        brand = combo_1.get()  # input('Введите марку автомобиля на английском ')
        model = l1_entry.get()  # input('Введите модель ')
        lowprice = combo_2.get()  # int(input('Введите примерную стоимость '))
        try:
            st = int(lowprice)
            minprice = st - 20000
            maxprice = st + 20000
        except ValueError:
            lowprice = ''
        a = 1

        if model == '':
            model = 'all'
        for j in range(1, 5):
            # a+=a
            # указываем url и get параметры запроса
            if lowprice == '':
                url = f'https://auto.drom.ru/{brand}/{model}/page{j}/'
            else:
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
                connection.commit()


# добавление в таблицу
def add():
    cursor.execute("SELECT * FROM car_search")
    i = 0
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", 'end', values=(row[0], row[1], row[2], row[3]))


# Поиск
def search():
    sqlite_update_table_query = 'DELETE from car_search'
    cursor.execute(sqlite_update_table_query)
    for i in tree.get_children():
        tree.delete(i)
    drom()
    add()


def print_selection(event):
    for selection in tree.selection():
        item = tree.item(selection)
        links = item["values"][3]
        webbrowser.open_new(links)


root = Tk()
root.title("Парсер. Зеваев Д.В. БИ-32. СГУГиТ 2021")
# # Меню
# menu = root.Menu()
#
# menu.add_command(label="О программе")
# menu.add_command(label="Выйти")
combo_1 = ttk.Combobox(root,
                       values=[
                           "audi",
                           "bmw",
                           "volvo",
                           "mercedes-benz"])

combo_1.grid(column=0, row=1, padx=6, pady=6)
combo_1.current(1)
combo_2 = ttk.Combobox(root,
                       values=[
                           200000,
                           400000,
                           700000,
                           1000000,
                           1500000])

combo_2.grid(column=0, row=5, padx=3, pady=3)
combo_2.current(1)
# текстовое поле и кнопка для добавления в список
lb_1 = Label(text='Выберите марку автомобиля')
lb_1.grid(column=0, row=0)
l1_entry = Entry(width=23)
l1_entry.grid(column=0, row=3, padx=2, pady=2)
lb_2 = Label(text='Введите модель автомобиля')
lb_2.grid(column=0, row=2)
lb_3 = Label(text='Выберите\введите стоимость')
lb_3.grid(column=0, row=4)
# add_button = Button(text="Заполнить таблицу", command=add, bg='lightblue').grid(column=0, row=7, padx=2, pady=2)
searchButton = Button(text="Поиск", command=search, bg='lightblue').grid(row=6, column=0, padx=2, pady=2)

# создаем таблицу
# сортировка по цене (Работает не правильно так как получаемое значение не верное
def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children()]
    l.sort(reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


tree = ttk.Treeview(columns=('carName', 'price', 'description', 'links'), show='headings')
tree.column('carName', width=120)
tree.column('price', width=70)
tree.column('description', width=350)
tree.column('links', width=350)
tree.bind("<<TreeviewSelect>>", print_selection)
tree.heading('carName', text='Название')
tree.heading('price', text='Стоимость', command=lambda: treeview_sort_column(tree, 'price', False))
tree.heading('description', text='Описание')
tree.heading('links', text='Ссылка')
# ysb = ttk.Scrollbar("", orient=VERTICAL, command=tree.yview())
# tree.configure(yscroll=ysb.set)
tree.grid(column=1, row=0, rowspan=10, padx=6, pady=6)


def callback(event):
    webbrowser.open_new(event.widget.cget("text"))


root.mainloop()
