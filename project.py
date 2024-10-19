from tkinter import *
from tkinter import messagebox
from datetime import date 
from datetime import datetime
'''import psycopg2
import pandas as pd
from psycopg2.extras import NamedTupleCursor
from json import load'''

#list_deposit = [['Сбер', '12 мес', '18%']] 
list_deposit = {
    'Сбер' : [12.5, 12.5, 18.5, 18.5, 18.5, 18.5, 20, 20, 20, 18, 18, 18, 14.5, 14.5, 12],
    'Т-банк' : [0, 17, 18, 18, 18, 18.3, 18, 18, 18, 18, 18, 18.38, 17.5, 17.67, 0],
    'Альфа' : [0, 0, 18, 19, 0, 20, 0, 0, 20, 0, 0, 21.1, 19.5, 19, 21],
    'ВТБ' : [0, 0, 17.7, 0, 0, 19.1, 0, 0, 0, 0, 0, 18.8, 16.9, 16.9, 14.4]
}

list_per_dep = [['Альфа', '4', '100000']]

# все вклады которые были созданы от 01.01.2024

def entrance():  # вход в личный кабинет
    window = Tk()
    window.title("ЛК")
    window.geometry("600x600")
    window.configure(bg='lightblue')
    login = str(login_input.get())
    # password = str(password_input.get())
    text_in = Label(window, text=f'Добро пожаловать в личный кабинет: {login}')
    text_in.pack(anchor=CENTER, expand=1)
    account_deposit(window)

def account_deposit(w):
    global list_per_dep
    if len(list_per_dep) == 0:
        text_deposit = Label(w, text='У вас нет вклада')
        text_deposit.pack(anchor=CENTER, expand=1.2)
        Button(w, text='Выбрать новый вклад', command=create_deposit).pack(pady=15)  ###
    else:
        text_deposit = Label(w, text=f'У вас есть вклады: {list_per_dep[0]}')
        text_deposit.pack(anchor=CENTER, expand=1.2)
        Button(w, text='Посчитать текущую прибыль', command=current_money).pack(pady=7)   
        Button(w, text='Выбрать новый вклад', command=create_deposit).pack(pady=15)   ###

def current_money():
    const_date = [5, 2024]
    window = Tk()
    window.title("Ваши вклады")
    window.geometry("600x600")
    window.configure(bg='lightblue')

    current_date = date.today()
    current_month = int(current_date.strftime("%m"))
    current_year = int(current_date.strftime("%Y"))
    delta = (current_year - const_date[1]) * 12 + current_month

    for deposit_data in list_per_dep:
        bank, months, initial_amount = deposit_data
        total_amount = int(initial_amount)

        if delta > int(months):
            for month in range(int(months)):
                interest_rate = list_deposit[bank][month % 12]  # Выбираем ставку для текущего месяца
                total_amount = (total_amount * interest_rate) / 100 + total_amount
            text_money = Label(window, text=f"У вас был вклад в {bank} на {months} месяцев: итоговая сумма составила {total_amount}")
            text_money.pack(anchor=CENTER)
        else:
            for month in range(delta):
                interest_rate = list_deposit[bank][month % 12]  # Выбираем ставку для текущего месяца
                total_amount = (total_amount * interest_rate) / 100 + total_amount
            text_money = Label(window, text=f"Для вклада в {bank} на {months} месяцев: итоговая сумма {total_amount}")
            text_money.pack(anchor=CENTER)

    window.mainloop()


def create_deposit():
    # Создаем новое окно для ввода данных о вкладе
    new_deposit_window = Tk()
    new_deposit_window.title("Создать новый вклад")

    # Создаем элементы для ввода данных
    bank_label = Label(new_deposit_window, text="Выберите банк:")
    bank_label.pack()
    bank_var = StringVar(new_deposit_window)
    bank_options = list(list_deposit.keys())  # Получаем список доступных банков из словаря
    bank_dropdown = OptionMenu(new_deposit_window, bank_var, *bank_options)
    bank_dropdown.pack()

    months_label = Label(new_deposit_window, text="Введите срок вклада (месяцы):")
    months_label.pack()
    months_entry = Entry(new_deposit_window)
    months_entry.pack()

    amount_label = Label(new_deposit_window, text="Введите сумму вклада:")
    amount_label.pack()
    amount_entry = Entry(new_deposit_window)
    amount_entry.pack()

    # Функция для сохранения данных о новом вкладе
    def save_deposit():
        global list_per_dep
        bank_selected = bank_var.get()
        months = int(months_entry.get())
        amount = int(amount_entry.get())
        list_per_dep.append([bank_selected, months, amount])
        new_deposit_window.destroy()  # Закрываем окно создания вклада
        account_deposit(window)  # Обновляем информацию о вкладах

    # Кнопка для сохранения данных
    save_button = Button(new_deposit_window, text="Сохранить", command=save_deposit)
    save_button.pack()

    new_deposit_window.mainloop()

'''def connect():  # подключение к БД
    global cfg
    conn = psycopg2.connect(
    host=cfg.get('host'),
    password=cfg.get('password'),
    user=cfg.get('user'),
    port = cfg.get('port'),
    database = cfg.get('database')
    )
    return conn

def create_table(conn,name, columns):  # создание таблицы
    cur = conn.cursor()
    request = f"create table {name} ({columns})"
    cur.execute(request)
    cur.execute("commit")
    cur.close()
 
def drop_table(conn, name):  # удаление таблицы
    cur = conn.cursor()
    cur.execute(f"drop table {name}")
    cur.execute("commit")
    cur.close()

def query(conn, request):  # получение информации из таблицы
    cur = conn.cursor()
    cur.execute(request)
    out = cur.fetchall()
    cur.close()
    return out

def login(username, password):  # вход пользователя
    print('login', username, password)
    init_table()
    conn = connect()
    realPass = ''
    try:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT password FROM users WHERE username=%s", (username,))
            sgbdrn = curs.fetchone()
            if sgbdrn is None:
                conn.close()
                return False
            realPass = sgbdrn[0]
    except e:
        print(e)
        conn.Close()
        return False
    conn.close()
    
    return password == realPass

def register(username, password):  # регистрация пользователя
    print('register', username, password)
    init_table()
    conn = connect()
    try:
        with     conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    except e:
        print(e)
        conn.close()
        return False
    conn.commit()
    conn.close()
    return True'''


window = Tk()
window.title('Финансовый аналитик')
window.geometry('400x300')
window.configure(bg='lightgreen')

frame = Frame(
    window,
    padx = 10,
    pady = 10
)
frame.pack(expand=True)

reg_login = Label(
    frame,
    text='Введите свой логин'
)
reg_login.grid(row=3, column=1)

reg_password = Label(
    frame,
    text='Введите свой пароль'
)
reg_password.grid(row=4, column=1)

login_input = Entry(
    frame,
)
login_input.grid(row=3, column=2)

password_input = Entry(
    frame,
)
password_input.grid(row=4, column=2, pady=5)

Button(text='Войти', command=entrance).pack(pady=20)

window.mainloop()