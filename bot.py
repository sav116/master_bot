import telebot
from telebot import types
import sqlite3
import time
import config, keyboard
from datetime import datetime, datetime, timedelta

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    userid = message.chat.id
    connect = sqlite3.connect('bot.db')
    q = connect.cursor()
    q.execute(""" CREATE TABLE IF NOT EXISTS client(
        id TEXT, surname TEXT, name1 TEXT,phone TEXT, cashback INTEGER, colvo INTEGER, adress TEXT
    ) """)
    q.execute("""CREATE TABLE IF NOT EXISTS problem(
        id TEXT, info TEXT
    )""")
    q.execute('''CREATE TABLE IF NOT EXISTS master_phone(
        id TEXT, phone TEXT
        )''')
    q.execute('''CREATE TABLE IF NOT EXISTS adm(
        id TEXT
        )''')
    connect.commit()
    res = q.execute("SELECT * FROM client where id is " + str(userid)).fetchone()
    if res is None:
        bot.send_message(message.chat.id, "<b>Немного о нас:\nBlack-Izi - это Сервисный центр по ремонту телефонов, планшетов, ноутбуков.\nМы осуществляем ремонт любой сложности.\nВ сферу наших услуг в том числе входят переклейка оригинальных модульных дисплеев по заводским технологиям, BGA пайка, разблокировка iCloud, Mi, Гугл аккаунтов.\nОпыт работы наших мастеров в данной сфере более 10 лет. На все виды работ даём гарантии от 1 месяца.\nРаботать с нами вдвойне выгодно, вам также начисляются cash back баллы.</b>",parse_mode='html', reply_markup=keyboard.reg)
    else:
        bot.send_message(userid, f"Пиветствую {message.from_user.username} в нашем боте", reply_markup=keyboard.profile)

@bot.message_handler(commands=['админ'])
def admin_menu(message):
    adm = []
    connect = sqlite3.connect('bot.db')
    q = connect.cursor()
    res = q.execute("SELECT * FROM adm").fetchall()
    for i in res:
        adm.append(i[0])
    if message.chat.id in config.admins or str(message.chat.id) in adm:
        bot.send_message(message.chat.id,"Админ панель", reply_markup=keyboard.admin)
    else:
        bot.send_message(message.chat.id,"Для вас эта команда недоступна")

@bot.message_handler(content_types=['text'])
def text_menu(message):
    if message.text == "Пользователи👤":
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        conenct = sqlite3.connect('bot.db')
        q = conenct.cursor()
        res = q.execute("SELECT * FROM client").fetchall()
        all_users = "Все зарегистрированые пользователи\n\n"
        for i in res:
            user = f"id - {i[0]}: Фамилия - {i[1]}: Имя - {i[2]}: Телефон - {i[3]}: Кэшбек - {i[5]}: Количество заказов {i[5]}: Адрес - {i[6]}"
            all_users = all_users + str(user) + "\n\n"
        bot.send_message(message.chat.id, all_users, reply_markup=keyboard.delete)
    
    if message.text == "Мой профиль👤":
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            userid = str(message.chat.id)
            conenct = sqlite3.connect('bot.db')
            q = conenct.cursor()
            res = q.execute(f"SELECT * FROM client where id = {userid}").fetchone()
            name = res[2]
            phone = res[3]
            cashback = res[4]
            colvo = res[5]
            adress = res[6]
            bot.send_message(userid,f"{name} это ваш профиль👨‍💻\n\n"\
                f"📲Ваш номер телефона: +{phone}\n"\
                    f"💲Кэшбек: {cashback} руб\n"\
                        f"⚙️Количество заказов: {colvo}\n"\
                            f"🏠Адрес вашей мастерсой: {adress}",reply_markup=keyboard.delete)
        except Exception as e:
            bot.send_message(config.coder, "❗️Произошла ошибка ПРОФИЛЬ 60❗️\n" \
                f"{e}")
    if message.text == "Установить номер📞":
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        send = bot.send_message(message.chat.id, "Введите номер☎️")
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(send, setphone)
    
    if message.text == "Назначить админа🦸":
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        send = bot.send_message(message.chat.id, "Введите id будущего админа🧞")
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(send, setadmin)
    
    if message.text == "Вернуться в меню👨‍💻":
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.send_message(message.chat.id, "Главное меню", reply_markup=keyboard.profile)
    
    if message.text == "Связаться с мастером🧑‍🔧":
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        connect = sqlite3.connect('bot.db')
        q = connect.cursor()
        res = q.execute("SELECT * FROM master_phone").fetchone()
        phone = res[1]
        bot.send_message(message.chat.id, "Есть какие-то вопросы⁉️\n"\
            f"Обращайтесь к нашему мастеру🧑‍🔧 {phone}", reply_markup=keyboard.delete)
    
    if message.text == "Сделать заказ⚙️":
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.send_message(message.chat.id, "Выберите способ отправки устройства", reply_markup=keyboard.dostavka)
    
    if message.text == "Узнать цену💵":
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        send = bot.send_message(message.chat.id, "Введите модель вашего устройства📲")
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(send, view_price)
    
    if message.text == "Вызвать курьера🏎":
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        now = datetime.now()
        work = now.replace(hour=13, minute=0, second=0, microsecond=0)
        now_date = datetime.now()
        if work >= now_date:
            bot.send_message(message.chat.id, "Выбирите устройство", reply_markup=keyboard.devices)
            
            delivery = "Курьер"
        else:
            bot.send_message(message.chat.id, "Отправка курьером возможна только до 13:00")
    
    if message.text in config.cura:
        config.delivery[message.chat.id] = message.text
    
    if message.text in config.sam:
        config.delivery[message.chat.id] = message.text
    
    if message.text == "Списать балы🙍":
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        send = bot.send_message(message.chat.id, "Введите айди пользователя которому нужно списать балы")
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(send,min_cashback)






    
    
    if message.text == "Приеду в мастерскую🔧":
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.send_message(message.chat.id, "Выбирите устройство", reply_markup=keyboard.devices)
    
    if message.text == "Начислить cashback💰":
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        send = bot.send_message(message.chat.id, "Введите айди пользователя которому нужно начислить cashback")
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(send,add_cashback)




        


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == "reg":
        send = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Введите свое ФИО",parse_mode="html")
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        bot.register_next_step_handler(send, register)
    
    if call.data == "delete":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    
    if call.data == "phone":
        send = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Введите количество",parse_mode="html")
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        bot.register_next_step_handler(send, next_step)
    
    if call.data == "tablet":
        send = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Введите количество",parse_mode="html")
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        bot.register_next_step_handler(send, next_step)
    
    if call.data == "laptop":
        send = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Введите количество",parse_mode="html")
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        bot.register_next_step_handler(send, diagnostic1)
    
    if call.data == "tv":
        send = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Введите количество",parse_mode="html")
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        bot.register_next_step_handler(send, diagnostic1)
    
    arr = call.data.split("_")
    if arr[0] == "send":
        try:

            connect = sqlite3.connect("bot.db")
            q = connect.cursor()
            res = q.execute(f"SELECT * FROM client where id = {call.message.chat.id}").fetchone()
            problem = q.execute(f"SELECT info FROM problem where id = {call.message.chat.id}").fetchone()[0]
            surname = res[1]
            name = res[2]
            phone = res[3]
            adress = res[6]

            bot.send_message(config.chat, "<b>❗️❗️Информация о заказе❗️❗️</b>\n\n"\
                f"👤ФИО: {surname} {name}\n"
                    f"📞Номер телефона: +{phone}\n"\
                        f"🌆Адрес мастерской: {adress}\n"\
                            f"📲Модель: {arr[1]}\n"\
                                f"🛒Количество: {arr[2]}\n"\
                                    f"📜Проблема: {problem}\n"\
                                        f"📦Доставка: {config.delivery[call.message.chat.id]}", parse_mode="html")
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(res[0], "Ваш заказ отправлен 📤")
            q.execute(f"DELETE FROM problem where id = {call.message.chat.id}")
            connect.commit()
            
        except Exception as e:
            bot.send_message(config.coder, "❗️Произошла ошибка ЗАЯВКА 144❗️\n"\
            f"{e}")




def diagnostic1(message):
    send = bot.send_message(message.chat.id,"Введите модель")
    bot.register_next_step_handler(send, diagnostic2)

def diagnostic2(message):
    send = bot.send_message(message.chat.id, "Опишите вашу проблему")
    bot.register_next_step_handler(send, diagnostic3)

def diagnostic3(message):
    bot.send_message(message.chat.id,"<b>Для более детальной информации по вашей модели, свяжитесь с нашим мастером</b>", parse_mode='html')


def setadmin(message):
    adm_id = message.text
    if adm_id.isdigit():
        try:
            connect = sqlite3.connect('bot.db')
            q = connect.cursor()
            res = q.execute(f"SELECT * FROM adm where id = {adm_id}").fetchone()
            if res is None:
                q.execute("INSERT INTO adm(id) VALUES ('%s')"%(adm_id))
                connect.commit()
                bot.send_message(message.chat.id, "Админ был успешно добавлен✅")
            
            bot.send_message(message.chat.id, "Админ уже добавлен😌")
        except:
            bot.send_message(message.chat.id, "Ошибка❗️")

            

    
    else:
        bot.send_message(message.chat.id, "Не корректное id❗️")


def next_step(message):
    colvo = message.text
    if colvo.isdigit():
        if int(colvo) <= 1:
            send = bot.send_message(message.chat.id, "Введите модель")
            bot.clear_step_handler_by_chat_id(message.chat.id)
            bot.register_next_step_handler(send, next_step1, colvo)
        else:
            send = bot.send_message(message.chat.id, "Введите ваши модели в вормате:\n"\
                "Модель 1\n"\
                    "Модель 2\n"\
                        "Медель ...")
            bot.clear_step_handler_by_chat_id(message.chat.id)
            bot.register_next_step_handler(send, next_step1, colvo)

    else:
        send = bot.send_message(message.chat.id, "Введите корректное количество")
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(send, next_step)
        

def next_step1(message, colvo):
    if int(colvo) <= 1:
        model = message.text
        send = bot.send_message(message.chat.id, "Опишите вашу проблему")
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(send, next_step2, colvo, model)
    else:
        model = message.text
        send = bot.send_message(message.chat.id, "Опишите ваши проблемы\n"\
            "Проблема 1\n"\
                "Проблема 2\n"\
                    "Проблема ...")
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(send, next_step2, colvo, model)


def next_step2(message, colvo, model):
    try:
        userid = message.chat.id
        conect = sqlite3.connect('bot.db')
        q = conect.cursor()
        res = q.execute(f"SELECT * FROM client where id = {userid}").fetchone()
        surname = res[1]
        name = res[2]
        phone = res[3]
        adress = res[6]
        colvo_zakazov = res[5]
        new_colvo = int(colvo_zakazov) + 1
        q.execute(f"update client set colvo = {new_colvo} where id = {userid}")
        conect.commit()
        problem = message.text
        q.execute("INSERT INTO problem(id, info) VALUES ('%s', '%s')"%(userid, problem))
        conect.commit()

        key = types.InlineKeyboardMarkup()
        send = types.InlineKeyboardButton("👍Отправить", callback_data="send_{}_{}".format(model, colvo))
        cancel = types.InlineKeyboardButton("❌Отменить",callback_data="delete")
        key.row(send, cancel)
        bot.send_message(userid,f"❗️❗️Информация о заказе❗️❗️\n\n"\
            f"👤ФИО: {surname} {name}\n"
                f"📞Номер телефона: +{phone}\n"\
                    f"🌆Адрес мастерской: {adress}\n"\
                        f"📲Модель: {model}\n"\
                            f"🛒Количество: {colvo}\n"\
                                f"📜Проблема: {problem}", parse_mode='html', reply_markup=key)


        
                            
    except Exception as e:
        bot.send_message(config.coder, "❗️Произошла ошибка ЗАЯВКА 144❗️\n"\
            f"{e}")




def register(message):
    try:
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True) 
        button_phone = types.KeyboardButton(text="Отправить телефон📞", request_contact=True) 
        keyboard.add(button_phone)
        bot.send_message(message.chat.id, 'Номер телефона', reply_markup=keyboard)
        userid = message.chat.id
        connect = sqlite3.connect('bot.db')
        q = connect.cursor()
        res = q.execute(f"SELECT * FROM client where id is " + str(userid)).fetchone()
        if res is None:
            data = message.text.split(" ")
            surname = str(data[0])
            name = str(data[1])
            cashback = 0
            colvo = 0
            q.execute("INSERT INTO client(id, surname,name1, cashback,colvo) VALUES ('%s','%s','%s','%s','%s')"%(userid, surname, name,cashback,colvo))
            connect.commit()
    except e:
        send = bot.send_message(message.chat.id, "Данные введены не корректно\n"\
            "<b>Формат ввода: Петров Виктор Александрович</b>", parse_mode='html')
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        bot.register_next_step_handler(send, register)
        

   
    

@bot.message_handler(content_types=['contact'])
def contact(message):
    try:
        userid = message.chat.id
        if message.contact is not None:
            phone = message.contact.phone_number
            connect = sqlite3.connect('bot.db')
            q = connect.cursor()
            res = q.execute(f"SELECT * FROM client where id = '{userid}'").fetchone()
            if res[3] is None:
                q.execute(f"update client set phone = {phone} where id = {userid}")
                connect.commit()
            send = bot.send_message(message.chat.id, "Введите адрес своей мастерской")
            bot.clear_step_handler_by_chat_id(message.chat.id)
            bot.register_next_step_handler(send, register1)
    except Exception as e:
        bot.send_message(config.coder, "❗️Произошла ошибка КОНТАКТЫ❗️\n"\
            f"{e}")

def register1(message):
    try:
        userid = message.chat.id
        adress = str(message.text)
        connect = sqlite3.connect('bot.db')
        q = connect.cursor()
        res = q.execute(f"SELECT * FROM client where id = '{userid}'").fetchone()
        if res[6] is None:
            q.execute(f"update client set adress = '{adress}' where id = {userid}")
            connect.commit()
            bot.send_message(userid, "<b>Регистрация прошла успешно</b>",parse_mode='html', reply_markup=keyboard.profile)
    except Exception as e:
        bot.send_message(config.coder, "❗️Произошла ошибка РЕГИСТРАЦИЯ❗️\n"\
            f"{e}")


def add_cashback(message):
    chat_id = message.text
    send = bot.send_message(message.chat.id, "Введите сумму кэшека для пользователя")
    bot.clear_reply_handlers_by_message_id(message.chat.id)
    bot.register_next_step_handler(send, add_money, chat_id)

def add_money(message, chat_id):
    summ = message.text
    if summ.isdigit():
        try:
            summ = int(summ)
            connect = sqlite3.connect('bot.db')
            q = connect.cursor()
            balik = q.execute(f"SELECT cashback FROM client where id = {chat_id}").fetchone()[0]
            balik = int(balik + summ)
            q.execute(f"update client set cashback = {balik} where id = {chat_id}")
            connect.commit()
            bot.send_message(message.chat.id, "Начисления прошло успешно✅")
            bot.send_message(chat_id, f"Вам начислен кэшбек в размере {summ} рублей")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка")
            
            bot.send_message(config.coder, "❗️Произошла ошибка НАЧИСЛЕНИЯ❗️\n"\
            f"{e}")
    else:
        bot.send_message(message.chat.id, "Введите корректные данные")

def min_cashback(message):
    chat_id = message.text
    connect = sqlite3.connect('bot.db')
    q = connect.cursor()
    bal = q.execute(f"SELECT cashback FROM client where id = {chat_id}").fetchone()[0]
    send = bot.send_message(message.chat.id, f"Введите сумму списания.\nДоступно {bal}руб")
    bot.clear_reply_handlers_by_message_id(message.chat.id)
    bot.register_next_step_handler(send, min_money, chat_id, bal)

def min_money(message, chat_id, bal):
    summ = message.text
    if summ.isdigit() and int(summ) <= int(bal):
        new_summ = int(bal) - int(summ)
        connect = sqlite3.connect('bot.db')
        q = connect.cursor()
        q.execute(f"update client set cashback = {new_summ} where id = {chat_id}")
        connect.commit()
        bot.send_message(message.chat.id, "Балы успешно списаны✅")
        bot.send_message(chat_id, f"У вас были списанны балы на сумму {summ}")
    else:
        bot.send_message(message.chat.id, "Не корректная сумма списания👿")



    

def setphone(message):
    try:
        new_phone = message.text
        user_id = message.chat.id
        connect = sqlite3.connect('bot.db')
        q = connect.cursor()
        res = q.execute("SELECT * FROM master_phone").fetchone()
        if res is None:
            q.execute("INSERT INTO master_phone (id, phone) VALUES ('%s', '%s')"%(user_id, new_phone))
            connect.commit()
        else:
            q.execute(f"update master_phone set phone = {new_phone} where id = {user_id}")
            connect.commit()
            
        bot.send_message(user_id, "Номер телефона установлен успешно")
    except:
        bot.send_message(user_id, "Произошла ошибка")


def view_price(message):
    model = message.text
    try:
        if model.lower() in config.iphone5:
            file = open("show_price/apple/iphone5.txt", "r",encoding="utf-8")
            lines = file.readlines()
            price = ""
            for i in lines:
                price = price + i + "\n"
            
            bot.send_message(message.chat.id, price, parse_mode="html", reply_markup=keyboard.delete)
            file.close()
        else:
            if model.lower() in config.iphone6:
                file = open("show_price/apple/iphone6.txt", "r",encoding="utf-8")
                lines = file.readlines()
                price = ""
                for i in lines:
                    price = price + i + "\n"
                
                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                file.close()
            else:
                if model.lower() in config.iphone6Plus:
                    file = open("show_price/apple/iphone6Plus.txt", "r",encoding="utf-8")
                    lines = file.readlines()
                    price = ""
                    for i in lines:
                        price = price + i + "\n"
                    
                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                    file.close()
                else:
                    if model.lower() in config.iphone6s:
                        file = open("show_price/apple/iphone6s.txt", "r",encoding="utf-8")
                        lines = file.readlines()
                        price = ""
                        for i in lines:
                            price = price + i + "\n"
                    
                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                        file.close()
                    else:
                        if model.lower() in config.iphone6sPlus:
                            file = open("show_price/apple/iPhone6splus.txt", "r",encoding="utf-8")
                            lines = file.readlines()
                            price = ""
                            for i in lines:
                                price = price + i + "\n"
                        
                            bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                            file.close()
                        else:
                            if model.lower() in config.iphone7:
                                file = open("show_price/apple/iPhone7.txt", "r",encoding="utf-8")
                                lines = file.readlines()
                                price = ""
                                for i in lines:
                                    price = price + i + "\n"
                            
                                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                file.close()
                            else:
                                if model.lower() in config.iphone7Plus:
                                    file = open("show_price/apple/iPhone7plus.txt", "r",encoding="utf-8")
                                    lines = file.readlines()
                                    price = ""
                                    for i in lines:
                                        price = price + i + "\n"
                                
                                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                    file.close()
                                else:
                                    if model.lower() in config.iphone8:
                                        file = open("show_price/apple/iPhone8.txt", "r",encoding="utf-8")
                                        lines = file.readlines()
                                        price = ""
                                        for i in lines:
                                            price = price + i + "\n"
                                    
                                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                        file.close()
                                    else:
                                        if model.lower() in config.iphone8Plus:
                                            file = open("show_price/apple/iPhone8plus.txt", "r",encoding="utf-8")
                                            lines = file.readlines()
                                            price = ""
                                            for i in lines:
                                                price = price + i + "\n"
                                        
                                            bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                            file.close()
                                        else:
                                            if model.lower() in config.iphoneX:
                                                file = open("show_price/apple/iPhoneX.txt", "r",encoding="utf-8")
                                                lines = file.readlines()
                                                price = ""
                                                for i in lines:
                                                    price = price + i + "\n"
                                            
                                                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                file.close()
                                            else:
                                                if model.lower() in config.iphoneXS:
                                                    file = open("show_price/apple/iPhoneXS.txt", "r",encoding="utf-8")
                                                    lines = file.readlines()
                                                    price = ""
                                                    for i in lines:
                                                        price = price + i + "\n"
                                                
                                                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                    file.close()
                                                else:
                                                    if model.lower() in config.iPhoneXSMAX:
                                                        file = open("show_price/apple/iPhoneXSMAX.txt", "r",encoding="utf-8")
                                                        lines = file.readlines()
                                                        price = ""
                                                        for i in lines:
                                                            price = price + i + "\n"
                                                    
                                                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                        file.close()
                                                    else:
                                                        if model.lower() in config.iPhoneXR:
                                                            file = open("show_price/apple/iPhoneXR.txt", "r",encoding="utf-8")
                                                            lines = file.readlines()
                                                            price = ""
                                                            for i in lines:
                                                                price = price + i + "\n"
                                                        
                                                            bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                            file.close()
                                                        else:
                                                            if model.lower() in config.iPhone11:
                                                                file = open("show_price/apple/iPhone11.txt", "r",encoding="utf-8")
                                                                lines = file.readlines()
                                                                price = ""
                                                                for i in lines:
                                                                    price = price + i + "\n"
                                                            
                                                                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                file.close()
                                                            else:
                                                                if model.lower() in config.iPhone11Pro:
                                                                    file = open("show_price/apple/iPhone11Pro.txt", "r",encoding="utf-8")
                                                                    lines = file.readlines()
                                                                    price = ""
                                                                    for i in lines:
                                                                        price = price + i + "\n"
                                                                
                                                                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                    file.close()
                                                                else:
                                                                    if model.lower() in config.iPhone11ProMax:
                                                                        file = open("show_price/apple/iPhone11ProMax.txt", "r",encoding="utf-8")
                                                                        lines = file.readlines()
                                                                        price = ""
                                                                        for i in lines:
                                                                            price = price + i + "\n"
                                                                    
                                                                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                        file.close()
                                                                    else:
                                                                        if model.lower() in config.watch:
                                                                            file = open("show_price/apple/watch.txt", "r",encoding="utf-8")
                                                                            lines = file.readlines()
                                                                            price = ""
                                                                            for i in lines:
                                                                                price = price + i + "\n"
                                                                        
                                                                            bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                            file.close()
                                                                        else:
                                                                            if "айпад" in model.lower() or "ipad" in model.lower():
                                                                                file = open("show_price/apple/ipad.txt", "r",encoding="utf-8")
                                                                                lines = file.readlines()
                                                                                price = ""
                                                                                for i in lines:
                                                                                    price = price + i + "\n"
                                                                            
                                                                                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                file.close()
                                                                            else:
                                                                                if model.lower() in config.samsungA10s:
                                                                                    file = open("show_price/samsung/samsungA10s.txt", "r",encoding="utf-8")
                                                                                    lines = file.readlines()
                                                                                    price = ""
                                                                                    for i in lines:
                                                                                        price = price + i + "\n"
                                                                                
                                                                                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                    file.close()
                                                                                else:
                                                                                    if model.lower() in config.samsungA10:
                                                                                        file = open("show_price/samsung/samsungA10.txt", "r",encoding="utf-8")
                                                                                        lines = file.readlines()
                                                                                        price = ""
                                                                                        for i in lines:
                                                                                            price = price + i + "\n"
                                                                                    
                                                                                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                        file.close()
                                                                                    else:
                                                                                        if model.lower() in config.samsungA20:
                                                                                            file = open("show_price/samsung/samsungA20.txt", "r",encoding="utf-8")
                                                                                            lines = file.readlines()
                                                                                            price = ""
                                                                                            for i in lines:
                                                                                                price = price + i + "\n"
                                                                                        
                                                                                            bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                            file.close()
                                                                                        else:
                                                                                            if model.lower() in config.samsungA20s:
                                                                                                file = open("show_price/samsung/samsungA20s.txt", "r",encoding="utf-8")
                                                                                                lines = file.readlines()
                                                                                                price = ""
                                                                                                for i in lines:
                                                                                                    price = price + i + "\n"
                                                                                            
                                                                                                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                file.close()
                                                                                            else:
                                                                                                if model.lower() in config.samsungA21s:
                                                                                                    file = open("show_price/samsung/samsungA21s.txt", "r",encoding="utf-8")
                                                                                                    lines = file.readlines()
                                                                                                    price = ""
                                                                                                    for i in lines:
                                                                                                        price = price + i + "\n"
                                                                                                
                                                                                                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                    file.close()
                                                                                                else:
                                                                                                    if model.lower() in config.samsungA3:
                                                                                                        file = open("show_price/samsung/samsungA3.txt", "r",encoding="utf-8")
                                                                                                        lines = file.readlines()
                                                                                                        price = ""
                                                                                                        for i in lines:
                                                                                                            price = price + i + "\n"
                                                                                                    
                                                                                                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                        file.close()
                                                                                                    else:
                                                                                                        if model.lower() in config.samsungA30:
                                                                                                            file = open("show_price/samsung/samsungA30.txt", "r",encoding="utf-8")
                                                                                                            lines = file.readlines()
                                                                                                            price = ""
                                                                                                            for i in lines:
                                                                                                                price = price + i + "\n"
                                                                                                        
                                                                                                            bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                            file.close()
                                                                                                        else:
                                                                                                            if "samsung a31" in model.lower() or "samsunga31" in model.lower() or "samsung a 31" in model.lower() or "самсунг a31" in model.lower():
                                                                                                                file = open("show_price/samsung/samsungA31.txt", "r",encoding="utf-8")
                                                                                                                lines = file.readlines()
                                                                                                                price = ""
                                                                                                                for i in lines:
                                                                                                                    price = price + i + "\n"
                                                                                                            
                                                                                                                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                file.close()
                                                                                                            else:
                                                                                                                if model.lower() in config.samsungA40:
                                                                                                                    file = open("show_price/samsung/samsungA40.txt", "r",encoding="utf-8")
                                                                                                                    lines = file.readlines()
                                                                                                                    price = ""
                                                                                                                    for i in lines:
                                                                                                                        price = price + i + "\n"
                                                                                                            
                                                                                                                
                                                                                                                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                    file.close()
                                                                                                                else:
                                                                                                                    if model.lower() in config.samsungA41:
                                                                                                                        file = open("show_price/samsung/samsungA41.txt", "r",encoding="utf-8")
                                                                                                                        lines = file.readlines()
                                                                                                                        price = ""
                                                                                                                        for i in lines:
                                                                                                                            price = price + i + "\n"
                                                                                                                    
                                                                                                                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                        file.close()
                                                                                                                    else:
                                                                                                                        if model.lower() in config.samsungA5:
                                                                                                                            file = open("show_price/samsung/samsungA5.txt", "r",encoding="utf-8")
                                                                                                                            lines = file.readlines()
                                                                                                                            price = ""
                                                                                                                            for i in lines:
                                                                                                                                price = price + i + "\n"
                                                                                                                        
                                                                                                                            bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                            file.close()
                                                                                                                        else:
                                                                                                                            if model.lower() in config.samsungA51:
                                                                                                                                file = open("show_price/samsung/samsungA51.txt", "r",encoding="utf-8")
                                                                                                                                lines = file.readlines()
                                                                                                                                price = ""
                                                                                                                                for i in lines:
                                                                                                                                    price = price + i + "\n"
                                                                                                                            
                                                                                                                                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                file.close()
                                                                                                                            else:
                                                                                                                                if model.lower() in config.samsungA6:
                                                                                                                                    file = open("show_price/samsung/samsungA6.txt", "r",encoding="utf-8")
                                                                                                                                    lines = file.readlines()
                                                                                                                                    price = ""
                                                                                                                                    for i in lines:
                                                                                                                                        price = price + i + "\n"
                                                                                                                                
                                                                                                                                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                    file.close()
                                                                                                                                else:
                                                                                                                                    if model.lower() in config.samsungA7:
                                                                                                                                        file = open("show_price/samsung/samsungA7.txt", "r",encoding="utf-8")
                                                                                                                                        lines = file.readlines()
                                                                                                                                        price = ""
                                                                                                                                        for i in lines:
                                                                                                                                            price = price + i + "\n"
                                                                                                                                    
                                                                                                                                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                        file.close()
                                                                                                                                    else:
                                                                                                                                        if model.lower() in config.samsungA70:
                                                                                                                                            file = open("show_price/samsung/samsungA70.txt", "r",encoding="utf-8")
                                                                                                                                            lines = file.readlines()
                                                                                                                                            price = ""
                                                                                                                                            for i in lines:
                                                                                                                                                price = price + i + "\n"
                                                                                                                                        
                                                                                                                                            bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                            file.close()
                                                                                                                                        else:
                                                                                                                                            if model.lower() in config.samsungA71:
                                                                                                                                                file = open("show_price/samsung/samsungA71.txt", "r",encoding="utf-8")
                                                                                                                                                lines = file.readlines()
                                                                                                                                                price = ""
                                                                                                                                                for i in lines:
                                                                                                                                                    price = price + i + "\n"
                                                                                                                                            
                                                                                                                                                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                file.close()
                                                                                                                                            else:
                                                                                                                                                if model.lower() in config.samsungA8:
                                                                                                                                                    file = open("show_price/samsung/samsungA8.txt", "r",encoding="utf-8")
                                                                                                                                                    lines = file.readlines()
                                                                                                                                                    price = ""
                                                                                                                                                    for i in lines:
                                                                                                                                                        price = price + i + "\n"
                                                                                                                                                
                                                                                                                                                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                    file.close()
                                                                                                                                                else:
                                                                                                                                                    if model.lower() in config.samsungA80:
                                                                                                                                                        file = open("show_price/samsung/samsungA80.txt", "r",encoding="utf-8")
                                                                                                                                                        lines = file.readlines()
                                                                                                                                                        price = ""
                                                                                                                                                        for i in lines:
                                                                                                                                                            price = price + i + "\n"
                                                                                                                                                    
                                                                                                                                                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                        file.close()
                                                                                                                                                    else:
                                                                                                                                                        if model.lower() in config.samsungA9:
                                                                                                                                                            file = open("show_price/samsung/samsungA9.txt", "r",encoding="utf-8")
                                                                                                                                                            lines = file.readlines()
                                                                                                                                                            price = ""
                                                                                                                                                            for i in lines:
                                                                                                                                                                price = price + i + "\n"
                                                                                                                                                        
                                                                                                                                                            bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                            file.close()
                                                                                                                                                        else:
                                                                                                                                                            if "samsung j2" in model.lower() or "самсунг j2" in model.lower():
                                                                                                                                                                file = open("show_price/samsung/samsungJ2.txt", "r",encoding="utf-8")
                                                                                                                                                                lines = file.readlines()
                                                                                                                                                                price = ""
                                                                                                                                                                for i in lines:
                                                                                                                                                                    price = price + i + "\n"
                                                                                                                                                            
                                                                                                                                                                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                file.close()
                                                                                                                                                            else:
                                                                                                                                                                if "samsung j3" in model.lower() or "самсунг j3" in model.lower():
                                                                                                                                                                    file = open("show_price/samsung/samsungJ3.txt", "r",encoding="utf-8")
                                                                                                                                                                    lines = file.readlines()
                                                                                                                                                                    price = ""
                                                                                                                                                                    for i in lines:
                                                                                                                                                                        price = price + i + "\n"
                                                                                                                                                                
                                                                                                                                                                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                    file.close()
                                                                                                                                                                else:
                                                                                                                                                                    if "samsung j4" in model.lower() or "самсунг j4" in model.lower():
                                                                                                                                                                        file = open("show_price/samsung/samsungJ4.txt", "r",encoding="utf-8")
                                                                                                                                                                        lines = file.readlines()
                                                                                                                                                                        price = ""
                                                                                                                                                                        for i in lines:
                                                                                                                                                                            price = price + i + "\n"
                                                                                                                                                                    
                                                                                                                                                                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                        file.close()
                                                                                                                                                                    else:
                                                                                                                                                                        if "samsung j5" in model.lower() or "самсунг j5" in model.lower():
                                                                                                                                                                            file = open("show_price/samsung/samsungJ5.txt", "r",encoding="utf-8")
                                                                                                                                                                            lines = file.readlines()
                                                                                                                                                                            price = ""
                                                                                                                                                                            for i in lines:
                                                                                                                                                                                price = price + i + "\n"
                                                                                                                                                                        
                                                                                                                                                                            bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                            file.close()
                                                                                                                                                                        else:
                                                                                                                                                                            if "samsung j6" in model.lower() or "самсунг j6" in model.lower():
                                                                                                                                                                                file = open("show_price/samsung/samsungJ6.txt", "r",encoding="utf-8")
                                                                                                                                                                                lines = file.readlines()
                                                                                                                                                                                price = ""
                                                                                                                                                                                for i in lines:
                                                                                                                                                                                    price = price + i + "\n"
                                                                                                                                                                            
                                                                                                                                                                                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                file.close()
                                                                                                                                                                            else:
                                                                                                                                                                                if "samsung j7" in model.lower() or "самсунг j7" in model.lower():
                                                                                                                                                                                    file = open("show_price/samsung/samsungJ7.txt", "r",encoding="utf-8")
                                                                                                                                                                                    lines = file.readlines()
                                                                                                                                                                                    price = ""
                                                                                                                                                                                    for i in lines:
                                                                                                                                                                                        price = price + i + "\n"
                                                                                                                                                                                
                                                                                                                                                                                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                    file.close()
                                                                                                                                                                                else:
                                                                                                                                                                                    if "samsung j8" in model.lower() or "самсунг j8" in model.lower():
                                                                                                                                                                                        file = open("show_price/samsung/samsungJ8.txt", "r",encoding="utf-8")
                                                                                                                                                                                        lines = file.readlines()
                                                                                                                                                                                        price = ""
                                                                                                                                                                                        for i in lines:
                                                                                                                                                                                            price = price + i + "\n"
                                                                                                                                                                                    
                                                                                                                                                                                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                        file.close()
                                                                                                                                                                                    else:
                                                                                                                                                                                        if "honor 7a" in model.lower() or "хонор 7а" in model.lower():
                                                                                                                                                                                            file = open("show_price/Huawei/Honor7A.txt", "r",encoding="utf-8")
                                                                                                                                                                                            lines = file.readlines()
                                                                                                                                                                                            price = ""
                                                                                                                                                                                            for i in lines:
                                                                                                                                                                                                price = price + i + "\n"
                                                                                                                                                                                        
                                                                                                                                                                                            bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                            file.close()
                                                                                                                                                                                        else:
                                                                                                                                                                                            if "honor 8" in model.lower() or "хонор 8" in model.lower():
                                                                                                                                                                                                file = open("show_price/Huawei/Honor8.txt", "r",encoding="utf-8")
                                                                                                                                                                                                lines = file.readlines()
                                                                                                                                                                                                price = ""
                                                                                                                                                                                                for i in lines:
                                                                                                                                                                                                    price = price + i + "\n"
                                                                                                                                                                                            
                                                                                                                                                                                                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                file.close()
                                                                                                                                                                                            else:
                                                                                                                                                                                                if "honor 9" in model.lower() or "хонор 9" in model.lower():
                                                                                                                                                                                                    file = open("show_price/Huawei/Honor9.txt", "r",encoding="utf-8")
                                                                                                                                                                                                    lines = file.readlines()
                                                                                                                                                                                                    price = ""
                                                                                                                                                                                                    for i in lines:
                                                                                                                                                                                                        price = price + i + "\n"
                                                                                                                                                                                                
                                                                                                                                                                                                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                    file.close()
                                                                                                                                                                                                else:
                                                                                                                                                                                                    if "honor 10" in model.lower() or "хонор 10" in model.lower():
                                                                                                                                                                                                        file = open("show_price/Huawei/Honor10.txt", "r",encoding="utf-8")
                                                                                                                                                                                                        lines = file.readlines()
                                                                                                                                                                                                        price = ""
                                                                                                                                                                                                        for i in lines:
                                                                                                                                                                                                            price = price + i + "\n"
                                                                                                                                                                                                    
                                                                                                                                                                                                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                        file.close()
                                                                                                                                                                                                    else:
                                                                                                                                                                                                        if "nova 3" in model.lower() or "нова 3" in model.lower():
                                                                                                                                                                                                            file = open("show_price/Huawei/nova3.txt", "r",encoding="utf-8")
                                                                                                                                                                                                            lines = file.readlines()
                                                                                                                                                                                                            price = ""
                                                                                                                                                                                                            for i in lines:
                                                                                                                                                                                                                price = price + i + "\n"
                                                                                                                                                                                                        
                                                                                                                                                                                                            bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                            file.close()
                                                                                                                                                                                                        else:
                                                                                                                                                                                                            if "p smart" in model.lower() or "п смарт" in model.lower():
                                                                                                                                                                                                                file = open("show_price/Huawei/Psmart.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                lines = file.readlines()
                                                                                                                                                                                                                price = ""
                                                                                                                                                                                                                for i in lines:
                                                                                                                                                                                                                    price = price + i + "\n"
                                                                                                                                                                                                            
                                                                                                                                                                                                                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                file.close()
                                                                                                                                                                                                            else:
                                                                                                                                                                                                                if "p9 lite" in model.lower() or "п9 лайт" in model.lower() or "p9" in model.lower() or "п9" in model.lower():
                                                                                                                                                                                                                    file = open("show_price/Huawei/P9.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                    lines = file.readlines()
                                                                                                                                                                                                                    price = ""
                                                                                                                                                                                                                    for i in lines:
                                                                                                                                                                                                                        price = price + i + "\n"
                                                                                                                                                                                                                
                                                                                                                                                                                                                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                    file.close()
                                                                                                                                                                                                                else:
                                                                                                                                                                                                                    if "p40 lite" in model.lower() or "п40 лайт" in model.lower() or "p40" in model.lower() or "п40" in model.lower():
                                                                                                                                                                                                                        file = open("show_price/Huawei/P40.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                        lines = file.readlines()
                                                                                                                                                                                                                        price = ""
                                                                                                                                                                                                                        for i in lines:
                                                                                                                                                                                                                            price = price + i + "\n"
                                                                                                                                                                                                                    
                                                                                                                                                                                                                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                        file.close()
                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                        if "p10 lite" in model.lower() or "п10 лайт" in model.lower() or "p10" in model.lower() or "п10" in model.lower():
                                                                                                                                                                                                                            file = open("show_price/Huawei/P10.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                            lines = file.readlines()
                                                                                                                                                                                                                            price = ""
                                                                                                                                                                                                                            for i in lines:
                                                                                                                                                                                                                                price = price + i + "\n"
                                                                                                                                                                                                                        
                                                                                                                                                                                                                            bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                            file.close()
                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                            if "p30 lite" in model.lower() or "п30 лайт" in model.lower() or "p30" in model.lower() or "п30" in model.lower():
                                                                                                                                                                                                                                file = open("show_price/Huawei/P30.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                lines = file.readlines()
                                                                                                                                                                                                                                price = ""
                                                                                                                                                                                                                                for i in lines:
                                                                                                                                                                                                                                    price = price + i + "\n"
                                                                                                                                                                                                                            
                                                                                                                                                                                                                                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                file.close()
                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                if "honor 20" in model.lower() or "хонор 20" in model.lower():
                                                                                                                                                                                                                                    file = open("show_price/Huawei/Honor20.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                    lines = file.readlines()
                                                                                                                                                                                                                                    price = ""
                                                                                                                                                                                                                                    for i in lines:
                                                                                                                                                                                                                                        price = price + i + "\n"
                                                                                                                                                                                                                                
                                                                                                                                                                                                                                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                    file.close()
                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                    if "mate" in model.lower():
                                                                                                                                                                                                                                        file = open("show_price/Huawei/HuaweiMate.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                        lines = file.readlines()
                                                                                                                                                                                                                                        price = ""
                                                                                                                                                                                                                                        for i in lines:
                                                                                                                                                                                                                                            price = price + i + "\n"
                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                        file.close()
                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                        if "nova" in model.lower() or "нова" in model.lower():
                                                                                                                                                                                                                                            file = open("show_price/Huawei/nova.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                            lines = file.readlines()
                                                                                                                                                                                                                                            price = ""
                                                                                                                                                                                                                                            for i in lines:
                                                                                                                                                                                                                                                price = price + i + "\n"
                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                            bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                            file.close()
                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                            if "nova 2" in model.lower() or "нова 2" in model.lower():
                                                                                                                                                                                                                                                file = open("show_price/Huawei/nova2.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                lines = file.readlines()
                                                                                                                                                                                                                                                price = ""
                                                                                                                                                                                                                                                for i in lines:
                                                                                                                                                                                                                                                    price = price + i + "\n"
                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                file.close()
                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                if "nova 2" in model.lower() or "нова 2" in model.lower():
                                                                                                                                                                                                                                                    file = open("show_price/Huawei/nova2.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                    lines = file.readlines()
                                                                                                                                                                                                                                                    price = ""
                                                                                                                                                                                                                                                    for i in lines:
                                                                                                                                                                                                                                                        price = price + i + "\n"
                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                    file.close()
                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                    if "honor 8a" in model.lower() or "хонор 8а" in model.lower():
                                                                                                                                                                                                                                                        file = open("show_price/Huawei/Honor8A.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                        lines = file.readlines()
                                                                                                                                                                                                                                                        price = ""
                                                                                                                                                                                                                                                        for i in lines:
                                                                                                                                                                                                                                                            price = price + i + "\n"
                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                        file.close()
                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                        if "y6" in model.lower() or "y 6" in model.lower():
                                                                                                                                                                                                                                                            file = open("show_price/Huawei/Y6.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                            lines = file.readlines()
                                                                                                                                                                                                                                                            price = ""
                                                                                                                                                                                                                                                            for i in lines:
                                                                                                                                                                                                                                                                price = price + i + "\n"
                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                            bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                            file.close()
                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                            if "redmi 3" in model.lower() or "редми 3" in model.lower():
                                                                                                                                                                                                                                                                file = open("show_price/xiaomi/Redmi3.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                                lines = file.readlines()
                                                                                                                                                                                                                                                                price = ""
                                                                                                                                                                                                                                                                for i in lines:
                                                                                                                                                                                                                                                                    price = price + i + "\n"
                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                                file.close()
                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                if "redmi 4" in model.lower() or "редми 4" in model.lower():
                                                                                                                                                                                                                                                                    file = open("show_price/xiaomi/Redmi4.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                                    lines = file.readlines()
                                                                                                                                                                                                                                                                    price = ""
                                                                                                                                                                                                                                                                    for i in lines:
                                                                                                                                                                                                                                                                        price = price + i + "\n"
                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                                    file.close()
                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                    if "redmi 5" in model.lower() or "редми 5" in model.lower():
                                                                                                                                                                                                                                                                        file = open("show_price/xiaomi/Redmi5.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                                        lines = file.readlines()
                                                                                                                                                                                                                                                                        price = ""
                                                                                                                                                                                                                                                                        for i in lines:
                                                                                                                                                                                                                                                                            price = price + i + "\n"
                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                                        file.close()
                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                        if "redmi 6" in model.lower() or "редми 6" in model.lower():
                                                                                                                                                                                                                                                                            file = open("show_price/xiaomi/Redmi6.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                                            lines = file.readlines()
                                                                                                                                                                                                                                                                            price = ""
                                                                                                                                                                                                                                                                            for i in lines:
                                                                                                                                                                                                                                                                                price = price + i + "\n"
                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                            bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                                            file.close()
                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                            if "redmi 7" in model.lower() or "редми 7" in model.lower() or "redmi note 7" in model.lower() or "редми нот 7" in model.lower():
                                                                                                                                                                                                                                                                                file = open("show_price/xiaomi/Redmi7.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                                                lines = file.readlines()
                                                                                                                                                                                                                                                                                price = ""
                                                                                                                                                                                                                                                                                for i in lines:
                                                                                                                                                                                                                                                                                    price = price + i + "\n"
                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                                                file.close()
                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                if "redmi 8" in model.lower() or "редми 8" in model.lower() or "redmi note 8" in model.lower() or "редми нот 8" in model.lower():
                                                                                                                                                                                                                                                                                    file = open("show_price/xiaomi/Redmi8.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                                                    lines = file.readlines()
                                                                                                                                                                                                                                                                                    price = ""
                                                                                                                                                                                                                                                                                    for i in lines:
                                                                                                                                                                                                                                                                                        price = price + i + "\n"
                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                                                    file.close()
                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                    if "redmi 9a" in model.lower() or "редми 9а" in model.lower() or "redmi 9c" in model.lower() or "редми 9с" in model.lower():
                                                                                                                                                                                                                                                                                        file = open("show_price/xiaomi/Redmi9a.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                                                        lines = file.readlines()
                                                                                                                                                                                                                                                                                        price = ""
                                                                                                                                                                                                                                                                                        for i in lines:
                                                                                                                                                                                                                                                                                            price = price + i + "\n"
                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                                                        file.close()
                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                        if "redmi 9" in model.lower() or "редми 9" in model.lower() or "redmi note 9" in model.lower() or "редми нот 9" in model.lower():
                                                                                                                                                                                                                                                                                            file = open("show_price/xiaomi/Redmi9.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                                                            lines = file.readlines()
                                                                                                                                                                                                                                                                                            price = ""
                                                                                                                                                                                                                                                                                            for i in lines:
                                                                                                                                                                                                                                                                                                price = price + i + "\n"
                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                            bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                                                            file.close()
                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                            if "mi a2 lite" in model.lower() or "ми а2 лайт" in model.lower():
                                                                                                                                                                                                                                                                                                file = open("show_price/xiaomi/MiA2lite.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                                                                lines = file.readlines()
                                                                                                                                                                                                                                                                                                price = ""
                                                                                                                                                                                                                                                                                                for i in lines:
                                                                                                                                                                                                                                                                                                    price = price + i + "\n"
                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                                                                file.close()
                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                if "redmi s2" in model.lower() or "редми с2" in model.lower():
                                                                                                                                                                                                                                                                                                    file = open("show_price/xiaomi/RedmiS2.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                                                                    lines = file.readlines()
                                                                                                                                                                                                                                                                                                    price = ""
                                                                                                                                                                                                                                                                                                    for i in lines:
                                                                                                                                                                                                                                                                                                        price = price + i + "\n"
                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                                                                    file.close()
                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                    if "mi a1" in model.lower() or "ми а1" in model.lower():
                                                                                                                                                                                                                                                                                                        file = open("show_price/xiaomi/MiA1.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                                                                        lines = file.readlines()
                                                                                                                                                                                                                                                                                                        price = ""
                                                                                                                                                                                                                                                                                                        for i in lines:
                                                                                                                                                                                                                                                                                                            price = price + i + "\n"
                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                                                                        file.close()
                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                        if "mi a1" in model.lower() or "ми а1" in model.lower():
                                                                                                                                                                                                                                                                                                            file = open("show_price/xiaomi/MiA1.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                                                                            lines = file.readlines()
                                                                                                                                                                                                                                                                                                            price = ""
                                                                                                                                                                                                                                                                                                            for i in lines:
                                                                                                                                                                                                                                                                                                                price = price + i + "\n"
                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                            bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                                                                            file.close()
                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                            if "mi a2" in model.lower() or "ми а2" in model.lower():
                                                                                                                                                                                                                                                                                                                file = open("show_price/xiaomi/MiA2.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                                                                                lines = file.readlines()
                                                                                                                                                                                                                                                                                                                price = ""
                                                                                                                                                                                                                                                                                                                for i in lines:
                                                                                                                                                                                                                                                                                                                    price = price + i + "\n"
                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                                                                                file.close()
                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                if "mi a3" in model.lower() or "ми а3" in model.lower():
                                                                                                                                                                                                                                                                                                                    file = open("show_price/xiaomi/MiA3.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                                                                                    lines = file.readlines()
                                                                                                                                                                                                                                                                                                                    price = ""
                                                                                                                                                                                                                                                                                                                    for i in lines:
                                                                                                                                                                                                                                                                                                                        price = price + i + "\n"
                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                                                                                    file.close()
                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                    if "mi a3" in model.lower() or "ми а3" in model.lower():
                                                                                                                                                                                                                                                                                                                        file = open("show_price/xiaomi/MiA3.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                                                                                        lines = file.readlines()
                                                                                                                                                                                                                                                                                                                        price = ""
                                                                                                                                                                                                                                                                                                                        for i in lines:
                                                                                                                                                                                                                                                                                                                            price = price + i + "\n"
                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                                                                                        file.close()
                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                        if "mi 6" in model.lower() or "ми 6" in model.lower() or "mi 6c" in model.lower() or "ми 6ц" in model.lower():
                                                                                                                                                                                                                                                                                                                            file = open("show_price/xiaomi/Mi6.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                                                                                            lines = file.readlines()
                                                                                                                                                                                                                                                                                                                            price = ""
                                                                                                                                                                                                                                                                                                                            for i in lines:
                                                                                                                                                                                                                                                                                                                                price = price + i + "\n"
                                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                            bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                                                                                            file.close()
                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                            if "mi 8" in model.lower() or "ми 8" in model.lower() or "mi 8 lite" in model.lower() or "ми 8 лайт" in model.lower():
                                                                                                                                                                                                                                                                                                                                file = open("show_price/xiaomi/Mi8.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                                                                                                lines = file.readlines()
                                                                                                                                                                                                                                                                                                                                price = ""
                                                                                                                                                                                                                                                                                                                                for i in lines:
                                                                                                                                                                                                                                                                                                                                    price = price + i + "\n"
                                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                                bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                                                                                                file.close()
                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                if "mi 9" in model.lower() or "ми 9" in model.lower() or "mi 9 lite" in model.lower() or "ми 9 лайт" in model.lower() or "mi 9t" in model.lower() or "ми 9т" in model.lower():
                                                                                                                                                                                                                                                                                                                                    file = open("show_price/xiaomi/Mi9.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                                                                                                    lines = file.readlines()
                                                                                                                                                                                                                                                                                                                                    price = ""
                                                                                                                                                                                                                                                                                                                                    for i in lines:
                                                                                                                                                                                                                                                                                                                                        price = price + i + "\n"
                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                    bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                                                                                                    file.close()
                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                    if "pocophone" in model.lower() or "покофон" in model.lower():
                                                                                                                                                                                                                                                                                                                                        file = open("show_price/xiaomi/Pocophone.txt", "r",encoding="utf-8")
                                                                                                                                                                                                                                                                                                                                        lines = file.readlines()
                                                                                                                                                                                                                                                                                                                                        price = ""
                                                                                                                                                                                                                                                                                                                                        for i in lines:
                                                                                                                                                                                                                                                                                                                                            price = price + i + "\n"
                                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                        bot.send_message(message.chat.id, price, parse_mode="html",reply_markup=keyboard.delete)
                                                                                                                                                                                                                                                                                                                                        file.close()
                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                        connect = sqlite3.connect('bot.db')
                                                                                                                                                                                                                                                                                                                                        q = connect.cursor()
                                                                                                                                                                                                                                                                                                                                        res = q.execute("SELECT * FROM master_phone").fetchone()
                                                                                                                                                                                                                                                                                                                                        phone = res[1]
                                                                                                                                                                                                                                                                                                                                        bot.send_message(message.chat.id, "<b>Ваша модель не найдена в базе</b>\n"\
                                                                                                                                                                                                                                                                                                                                            f"Обратитесь к нашему мастеру {phone}", reply_markup='html')
    except:
        connect = sqlite3.connect('bot.db')
        q = connect.cursor()
        res = q.execute("SELECT * FROM master_phone").fetchone()
        phone = res[1]
        bot.send_message(message.chat.id, "<b>Возниклы трудности с поиском вашей модели</b>\n"\
            f"Обратитесь к нашему мастеру {phone}", reply_markup='html')




















                                                                                                                                                                            











                                                













        



while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(e)

        time.sleep(15)