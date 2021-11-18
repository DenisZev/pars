from tkinter import *
import sqlite3

window = Tk()
window.title("Сравнение цен.")
lbl = Label(window, text="Привет")
# lbl.grid(column=3, row=3)
# window.geometry('600x300')
frame = Listbox(window)

connection = sqlite3.connect('mashinki.db')
cursor = connection.cursor()
connection.commit()
cursor.execute("SELECT * FROM car_search")
scroll = Scrollbar(command=frame.yview)
scroll.pack(side=LEFT, fill=Y)
frame.config(yscrollcommand=scroll.set)
# class ListFrame(window.Frame):
#     def __init__(self, master, items=[]):
#         super().__init__(master)
#         self.list = window.Listbox(self)
#         self.scroll = window.Scrollbar(self, orient=window.VERTICAL,
#                                    command=self.list.yview)
#         self.list.config(yscrollcommand=self.scroll.set)
#         self.list.insert(0, *items)
#         self.list.pack(side=window.LEFT)
#         self.scroll.pack(side=window.LEFT, fill=window.Y)

def click_button():
    i=0
    rows = cursor.fetchall()
    for row in rows:
        for j in range(len(row)):
            e = Entry(window, fg='blue', width=len(row))
            e.grid(row=i, column=j)
            e.insert(END, row[j])
        i = i + 1
        # print(row)

btn = Button(window, text="искать", command=click_button)
btn.place(x=10, y=50)

window.mainloop()
