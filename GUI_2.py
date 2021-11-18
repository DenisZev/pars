from tkinter import *
from tkinter import ttk
import sqlite3

# соединение с базой данных
connection = sqlite3.connect('mashinki.db')
cursor = connection.cursor()
connection.commit()
cursor.execute("SELECT * FROM car_search")


# удаление выделенного элемента
def delete():
    selection = languages_listbox.curselection()
    # мы можем получить удаляемый элемент по индексу
    # selected_language = languages_listbox.get(selection[0])
    languages_listbox.delete(selection[0])


# добавление нового элемента
def add():
    new_language = l1_entry.get()
    # languages_listbox.insert(0, new_language)
    i = 0
    rows = cursor.fetchall()
    for row in rows:
        for j in range(len(row)):
            e = Entry(new_language, fg='blue', width=len(row))
            # e.grid(row=i, column=j)
            languages_listbox.insert(END, row[j])
        i = i + 1


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
languages_listbox = Listbox()
languages_listbox.grid(row=4, column=0, columnspan=3, sticky=W + E, padx=10, pady=10)

# добавляем в список начальные элементы
# languages_listbox.insert(END, "Python")
# languages_listbox.insert(END, "C#")

delete_button = Button(text="Удалить", command=delete).grid(row=2, column=1, padx=5, pady=5)

root.mainloop()
