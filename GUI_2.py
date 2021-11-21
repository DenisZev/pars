from tkinter import *
from tkinter import ttk
import sqlite3
import requests
from bs4 import BeautifulSoup
# соединение с базой данных
connection = sqlite3.connect('mashinki.db')
cursor = connection.cursor()
connection.commit()
cursor.execute("SELECT * FROM car_search")

class drom(object):

    def __init__(self):
        brand = combo_1.get()  # input('Введите марку автомобиля на английском ')
        model = l1_entry.get()  # input('Введите модель ')
        lowprice = int(combo_2.get())  # int(input('Введите примерную стоимость '))
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
                connection.commit()

# удаление выделенного элемента
# def delete():
    # selection = languages_listbox.curselection()
    # мы можем получить удаляемый элемент по индексу
    # selected_language = languages_listbox.get(selection[0])
    # languages_listbox.delete(selection[0])


# добавление нового элемента
def add():
    # new_language = l1_entry.get()
    # languages_listbox.insert(0, new_language)
    i = 0
    rows = cursor.fetchall()

    for row in rows:
        for j in range(len(row)):
            # e = Entry(new_language, fg='blue', width=len(row))
            # e.grid(row=i, column=j)
            tree.insert('', 'end', values=(row[0], row[1], row[2], row[3]))
        i = i + 1


# box_value = StringVar()


def run():
    drom()
    add()
root = Tk()
root.title("Поиск машин")

combo_1 = ttk.Combobox(root,
                       values=[
                           "audi",
                           "bmw",
                           "volvo",
                           "mercedes"])

combo_1.grid(column=0, row=1)
combo_1.current(1)
combo_2 = ttk.Combobox(root,
                       values=[
                           200000,
                           400000,
                           700000,
                           1000000,
                           1500000])

combo_2.grid(column=1, row=1)
combo_2.current(1)
# текстовое поле и кнопка для добавления в список
lb_1 = Label(text='Введите марку автомобиля')
lb_1.grid(column=0, row=0)
l1_entry = Entry(width=23)
l1_entry.grid(column=0, row=3, padx=6, pady=6)
lb_2 = Label(text='Введите модель автомобиля')
lb_2.grid(column=0, row=2)
lb_3 = Label(text='Выберите стоимость')
lb_3.grid(column=1, row=0)
add_button = Button(text="Поиск", command=add).grid(column=2, row=3, padx=6, pady=6)

# создаем список
# languages_listbox = Listbox()
# languages_listbox.grid(row=4, column=0, columnspan=3, sticky=W + E, padx=10, pady=10)
tree = ttk.Treeview(columns=('carName', 'price', 'description', 'links'))
tree.column('#0')
tree.column('price')
tree.column('description')
tree.column('links')
tree.heading('carName', text='Название')
tree.heading('price', text='Стоимость')
tree.heading('description', text='Описание')
tree.heading('links', text='Ссылка')

tree.grid(column=0, row=5)
# добавляем в список начальные элементы
# languages_listbox.insert(END, "Python")
# languages_listbox.insert(END, "C#")

delete_button = Button(text="Удалить", command=run).grid(row=2, column=1, padx=5, pady=5)

root.mainloop()
