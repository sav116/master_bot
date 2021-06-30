import telebot
from telebot import types

reg = types.InlineKeyboardMarkup()
reg.row(types.InlineKeyboardButton("Зарегистрироваться✅", callback_data="reg"))

admin = types.ReplyKeyboardMarkup(True)
admin.add("Пользователи👤","Начислить cashback💰")
admin.add("Установить номер📞","Назначить админа🦸")
admin.add("Списать балы🙍","Вернуться в меню👨‍💻")

a = '🙊'
profile = types.ReplyKeyboardMarkup(True)
profile.add("Сделать заказ⚙️","Мой профиль👤")
profile.add("Связаться с мастером🧑‍🔧", "Узнать цену💵")

dostavka = types.ReplyKeyboardMarkup(True)
dostavka.add("Вызвать курьера🏎", "Приеду в мастерскую🔧")
dostavka.add("Вернуться в меню👨‍💻")

delete = types.InlineKeyboardMarkup()
del1 = types.InlineKeyboardButton("❌Закрыть",callback_data="delete")
delete.row(del1)


devices = types.InlineKeyboardMarkup()
phone = types.InlineKeyboardButton("📱Телефон", callback_data="phone")
tablet = types.InlineKeyboardButton("📲Планшет", callback_data="tablet")
laptop = types.InlineKeyboardButton("💻Ноутбук", callback_data="laptop")
tv = types.InlineKeyboardButton("🖥Телевизор", callback_data="tv")
devices.row(phone,tablet)
devices.row(laptop,tv)
devices.row(del1)
