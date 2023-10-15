import tkinter as tk
from tkinter import ttk,messagebox
import sqlite3,time
# класс главного окна
lastact = ''


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        global lastact
        #панель интсуремнотв
        toolbar = tk.Frame(bg='#d7d7d7', bd=4)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        #создание картинки
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btd_add = tk.Button(toolbar, bg='#d7d7d7',bd=0,text='Добавить сотрудника',command=self.open_dialog)
        btd_add.pack(side=tk.LEFT)
        btd_del = tk.Button(toolbar, bg='#d7d7d7',bd=0,text='Удалить сотрудника',command=self.deletecontact)
        btd_del.pack(side=tk.LEFT)
        self.search = tk.Entry(toolbar, width=30)
        btd_search = tk.Button(toolbar, bg='#d7d7d7',bd=0,text='Поиск',image=self.search_img)
        btd_search.pack(side=tk.LEFT)
        self.search.pack(side=tk.LEFT)
        btd_search.bind('<Button-1>',lambda ev: self.searching(self.search.get()))

        btd_del = tk.Button(toolbar, bg='#d7d7d7',bd=0,text='Обновить таблицу',command=self.view_records)
        btd_del.pack(side=tk.LEFT)

        #создание таблицы
        self.tree = ttk.Treeview(root, columns=('id','name','tel','email','zarplata'),height=45,show='headings')

        #добавляем параметры столбцам
        self.tree.column('id', width=45,anchor=tk.CENTER)
        self.tree.column('name', width=300,anchor=tk.CENTER)
        self.tree.column('tel', width=150,anchor=tk.CENTER)
        self.tree.column('email', width=150,anchor=tk.CENTER)
        self.tree.column('zarplata', width=80,anchor=tk.CENTER)

        self.tree.heading('id',text='id')
        self.tree.heading('name',text='ФИО')
        self.tree.heading('tel',text='Телефон')
        self.tree.heading('email',text='E-mail')
        self.tree.heading('zarplata',text='Зарплата')

        self.tree.pack(side=tk.LEFT)

    #метод добавления в бд
    def records(self,name,tel,email,zarplata):
        self.db.insert_data(name,tel,email,zarplata)
        self.view_records()
    #вызов дочерного окна
    def open_dialog(self):
        Child()
    def searching(self,fio):
        global lastact
        for i in self.tree.get_children():
            if self.tree.item(i).get('values')[1] == fio:
                self.tree.selection_add(i)
                lastact = f"Найдено совпадение с id {self.tree.set(i,'#1') }"

    def deletecontact(self):
        global lastact
        print(self.tree.index(self.tree.focus()))
        print(self.tree.selection())
        if self.tree.selection()!=():
            deletes = list()
            for i in self.tree.selection():
                deletes.append(self.tree.set(i,'#2'))
            if messagebox.askyesno('Удаление контактов?',f'Уверены что хотите удалить {deletes}',):

                # db.delete_data(self.tree.index(self.tree.focus())+
                for i in self.tree.selection():
                    oneid=self.tree.set(i,'#1')
                    db.cur.execute(f"""
                        DELETE FROM users
                        WHERE id = ?
                    """,(oneid,))
                self.db.conn.commit()
                self.view_records()

        lastact = f'Удален сотрудник(и)'

    def view_records(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
        self.db.cur.execute('SELECT * FROM users')
        [self.tree.insert('','end',values=i) for i in self.db.cur.fetchall()]
# класс дочеренего окна
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app


    def init_child(self):
        global lastact
        self.title('Добавление контакта')
        self.geometry('400x220')
        self.resizable(False,False)
        #перехватываем события приложения
        self.grab_set()
        #захватываем фокус
        self.focus_set()

        #создание формы
        label_name = tk.Label(self,text='ФИО')
        label_name.place(x=50,y=50)
        label_tel = tk.Label(self,text='Телефон')
        label_tel.place(x=50,y=80)
        label_email = tk.Label(self,text='Email')
        label_email.place(x=50,y=110)
        label_email = tk.Label(self,text='Зарплата')
        label_email.place(x=50,y=140)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200,y=50)
        self.entry_tel = tk.Entry(self)
        self.entry_tel.place(x=200,y=80)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200,y=110)
        self.entry_zarplata = tk.Entry(self)
        self.entry_zarplata.place(x=200,y=140)

        btn_ok = tk.Button(self,text='Добавить')
        btn_ok.place(x=280,y=190)
        btn_ok.bind('<Button-1>',lambda ev: self.view.records(self.entry_name.get(),self.entry_tel.get(),self.entry_email.get(),self.entry_zarplata.get()))
        btn_nop = tk.Button(self,text='Закрыть',command=self.destroy)
        btn_nop.place(x=220,y=190)
        lastact = f'Добавлен сотрудник {self.entry_name.get()}'
# класс бд
class Db:
    def __init__(self):
        self.conn = sqlite3.connect('contancts.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    phone TEXT,
                    email TEXT,
                    zarplata INTEGER
        )
        ''')
    # метод добавления в базу данных
    def insert_data(self,name,tel,email,zarplata):
        self.cur.execute('''
                    INSERT INTO users (name,phone,email,zarplata)
                    VALUES (?,?,?,?)''',(name,tel,email,zarplata)
        )
        self.conn.commit()

    def delete_data(self,id):
        print(id,1000)



#действия при запуске программы
if __name__ == '__main__':
    root = tk.Tk()
    db = Db()
    app = Main(root)
    root.title('Список сотрудников компании')
    root.geometry('745x400')
    root.resizable(False,False)

    root.mainloop()