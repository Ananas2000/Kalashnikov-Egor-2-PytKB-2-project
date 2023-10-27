import tkinter as tk        # Импорт библиотеки tkinter
from tkinter import ttk     # Импорт ttk из библиотеки tkinter
import sqlite3              # Импортируем  библиотеку sqlite3


class Main(tk.Frame):
    def __init__(self, root):                               # Конструктор класса
        super().__init__(root)                              
        self.init_main()                                    
        self.db = db                                        
        self.view_records()                                 

    def init_main(self):                                    # Метод со всеми графическими элементами(поля,кнопки)

        #Frame = виджет для группировки и организации других виджетов в окне приложения
        toolbar = tk.Frame(bg="#d7d8e0", bd=2)             
        toolbar.pack(side=tk.TOP, fill=tk.X)              


        self.add_img = tk.PhotoImage(file="./img/add.png")  # Загрузка изображения кнопки добавление в переменнную
        # Создание кнопки
        btn_open_dialog = tk.Button(
            toolbar, bg="#d7d8e0", bd=0, image=self.add_img, command=self.open_dialog
        )
        btn_open_dialog.pack(side=tk.LEFT)                 

        # Создание таблиц с колонками:"ID", "name", "tel", "email"
        self.tree = ttk.Treeview(
            self, columns=("ID", "name", "tel", "email","salary"), height=45, show="headings"
        )

        self.tree.column("ID", width=30, anchor=tk.CENTER)          
        self.tree.column("name", width=300, anchor=tk.CENTER)       
        self.tree.column("tel", width=150, anchor=tk.CENTER)        
        self.tree.column("email", width=150, anchor=tk.CENTER)      
        self.tree.column("salary", width=90, anchor=tk.CENTER)      

        self.tree.heading("ID", text="ID")                          
        self.tree.heading("name", text="ФИО")                      
        self.tree.heading("tel", text="Телефон")                   
        self.tree.heading("email", text="E-mail")                  
        self.tree.heading("salary", text="Зарплата")                 

        self.tree.pack(side=tk.LEFT)                                # Размещение таблицы в окне


        self.update_img = tk.PhotoImage(file="./img/update.png")    # Загрузка изображения кнопки обновления в переменнную
        # Создание кнопки
        btn_edit_dialog = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.update_img,
            command=self.open_update_dialog,
        )
        btn_edit_dialog.pack(side=tk.LEFT)                          


        self.delete_img = tk.PhotoImage(file="./img/delete.png")    # Загрузка изображения кнопки обновления в переменнную
        # Создание кнопки
        btn_delete = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.delete_img,
            command=self.delete_records,
        )
        btn_delete.pack(side=tk.LEFT)                              


        
        self.search_img = tk.PhotoImage(file="./img/search.png")    # Загрузка изображения кнопки обновления в переменнную
        # Создание кнопки
        btn_search = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.search_img,
            command=self.open_search_dialog,
        )
        btn_search.pack(side=tk.LEFT)                                                   

    def open_dialog(self):                                                             
        Child()                                                                        

    def records(self, name, tel, email,salary ):
        self.db.insert_data(name, tel, email,salary )                                   
        self.view_records()                                                         

    def view_records(self):
        self.db.cursor.execute("SELECT * FROM Employees")                               
        [self.tree.delete(i) for i in self.tree.get_children()]                         
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()] 

    def open_update_dialog(self):
        Update()                                                                      

    def update_records(self, name, tel, email, salary):
        self.db.cursor.execute(                                                         
            """UPDATE Employees SET name=?, tel=?, email=?, salary=? WHERE id=?""",

          
            (name, tel, email,salary, self.tree.set(self.tree.selection()[0], "#1")),
        )
        self.db.conn.commit()                                                          
        self.view_records()                                                            

    def delete_records(self):
        for selection_items in self.tree.selection():
            self.db.cursor.execute(                                            
                "DELETE FROM Employees WHERE id=?", (self.tree.set(selection_items, "#1"))    
            )
        self.db.conn.commit()                                                          
        self.view_records()                                                            

    def open_search_dialog(self):
        Search()                                                                       

    def search_records(self, name):
        name = "%" + name + "%"                                                        
        self.db.cursor.execute("SELECT * FROM Employees WHERE name LIKE ?", (name,))   

        [self.tree.delete(i) for i in self.tree.get_children()]                        
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]  


class Child(tk.Toplevel):                                   # Дочерний класс
    def __init__(self):  
        super().__init__(root)              
        self.init_child()                        
        self.view = app

    def init_child(self):
        self.title("Добавить сотрудника")              
        self.geometry("400x220")                     
        self.resizable(False, False)                  

        self.grab_set()                                     # Захват пользовательского ввода
        self.focus_set()                                    # Установка фокуса на нужном виджете, когда основное окно находится в фокусе

        label_name = tk.Label(self, text="ФИО:")            # Создание формы для ФИО
        label_name.place(x=50, y=50)                
        label_select = tk.Label(self, text="Телефон:")      # Создание формы для Телефона
        label_select.place(x=50, y=80)                
        label_sum = tk.Label(self, text="E-mail:")          # Создание формы для E-mail
        label_sum.place(x=50, y=110)                    

        label_salary = tk.Label(self, text="Зарплата:")          # Создание формы для E-mail
        label_salary.place(x=50, y=140)                 


        self.entry_name = ttk.Entry(self)                   # Поле для ввода формы ФИО
        self.entry_name.place(x=200, y=50)                
        self.entry_email = ttk.Entry(self)                  # Поле для ввода формы  E-mail
        self.entry_email.place(x=200, y=80)                
        self.entry_tel = ttk.Entry(self)                    # Поле для ввода формы Телефон
        self.entry_tel.place(x=200, y=110)                

        self.entry_salary = ttk.Entry(self)                    # Поле для ввода формы Телефон
        self.entry_salary.place(x=200, y=140)                  

        # Кнопка закрытия дочернего класса.
        # self.destroy - закрытие окна

        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=220, y=170)

        # Кнопка для добавления текста и её расположение
        self.btn_ok = ttk.Button(self, text="Добавить")
        self.btn_ok.place(x=300, y=170)

        # Отслеживание события, при котором сработает кнопка ДОБАВИТЬ
        # Нажатием левой кнопкой мыши по этой кнопке вызывается функция records и ей передается информация из полей: name, email, tel
        self.btn_ok.bind(
            "<Button-1>",
            lambda event: self.view.records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get(), self.entry_salary.get()
            ),
        )


class Update(Child):
    def __init__(self):                                             # Конструктор класса
        super().__init__()                        
        self.init_edit()                                  
        self.view = app                                
        self.db = db                                        
        self.default_data()                          

    #Метод редактирования данных в бд
    def init_edit(self):
        self.title("Редактирование данных сотрудника")            
        btn_edit = ttk.Button(self, text="Редактировать")       
        btn_edit.place(x=205, y=170)                             

        #Отслеживание события, при котором сработает кнопка ИЗМЕНИТЬ
        #Нажатием левой кнопкой мыши по этой кнопке вызывается функция update_records и ей передается информация из полей: name, email, tel
        btn_edit.bind(
            "<Button-1>",
            lambda event: self.view.update_records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get(), self.entry_salary.get()
            ),
        )

        #Отслеживание события, при котором сработает кнопка 
        btn_edit.bind(
            "<Button-1>",
            lambda event: self.destroy(), add="+"
        )

        self.btn_ok.destroy()                                               #Закрытие кнопки btn_ok

    def default_data(self):
        self.db.cursor.execute(                                             # Запрос на выбор всех полей с id
            "SELECT * FROM Employees WHERE id=?",
            self.view.tree.set(self.view.tree.selection()[0], "#1"),        # Выбор id выделенной строки
        )
        row = self.db.cursor.fetchone()                         # Получение первой записи
        self.entry_name.insert(0, row[1])                       # Передача значения в поле из этой записи
        self.entry_email.insert(0, row[2])                      # Передача значения в поле из этой записи
        self.entry_tel.insert(0, row[3])                        # Передача значения в поле из этой записи
        self.entry_salary.insert(0,row[4])



class Search(tk.Toplevel):
    def __init__(self):                                         # Конструктор класса
        super().__init__()                                    
        self.init_search()                                    
        self.view = app                                     

    def init_search(self):
        self.title("Поиск сотрудника")                       
        self.geometry("300x100")                              
        self.resizable(False, False)                          

        label_search = tk.Label(self, text="Имя:")              #Формы для поиска ФИО
        label_search.place(x=50, y=20)                          

        self.entry_search = ttk.Entry(self)                     #Поле для ввода формы поиска по  ФИО
        self.entry_search.place(x=100, y=20, width=150)         

        # Создание кнопки
        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=185, y=50)

        # Создание кнопки
        search_btn = ttk.Button(self, text="Найти")
        search_btn.place(x=105, y=50)

        #Отслеживание события, при котором сработает кнопка ПОИСК

        search_btn.bind(
            "<Button-1>",
            lambda event: self.view.search_records(self.entry_search.get()),
        )
        #Отслеживание события, при котором сработает кнопка

        search_btn.bind("<Button-1>", lambda event: self.destroy(), add="+")



class DB:
    def __init__(self):                                                                 # Конструктор класса
        self.conn = sqlite3.connect("db.db")                                            # Создание соединения с базой данных(имя бд)
        self.cursor = self.conn.cursor()                                          
        self.cursor.execute(                                                            # Запрос на создание бд
            '''
            CREATE TABLE IF NOT EXISTS Employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            tel TEXT NOT NULL,
            email TEXT NOT NULL,
            salary INTEGER
            )
            '''
        )
        self.conn.commit()                                                              # Сохранение запроса
        self.data()

    # Метод добавленияя изначальных данных в бд
    def data(self):
        insert_into = 'INSERT INTO Employees (name, tel, email, salary) VALUES (?, ?, ?, ?)'


        user_data=('Pavel', '+19884441502', 'barabushja@gmail.com','120')
        user_data1=('Grisha', '+79886602396', 'barebuh365@gmail.com','120')
        user_data2=('Inokentiy', '+19886489125', 'kokajokapix34@yandex.com','120')
        user_data3=('Fedya', '+79889561238', 'vanillka90@gmail.com','120')
        user_data4=('Nazariy', '88005553535', 'friedbebra98@yandex.com','120')
        self.cursor.execute(insert_into,user_data )
        self.cursor.execute(insert_into,user_data1 )
        self.cursor.execute(insert_into,user_data2 )
        self.cursor.execute(insert_into,user_data3 )
        self.cursor.execute(insert_into,user_data4 )

        self.conn.commit()                                                                                          # Сохранение запроса


    def insert_data(self, name, tel, email, salary):                                                                # Метод добавленияя данных в таблицу
        self.cursor.execute(                                                                                        # Запрос на создание базы данных
            """INSERT INTO Employees(name, tel, email, salary) VALUES(?, ?, ?, ?)""", (name, tel, email, salary) 
        )
        self.conn.commit()                                                                                          # Сохранение запроса

if __name__ == "__main__":
    root = tk.Tk()                                  # Экземпляр Tk
    db = DB()                                
    app = Main(root)                         
    app.pack()                                      # Размещение app в окне
    root.title("Список сотрудников компании")       # Заголовок экземпляра Tk
    root.geometry("765x450")                     
    root.resizable(False, False)                    # Ограничения изменеия размеров окна
    root.mainloop()                                 # Запуск основного цикла обработки событий
