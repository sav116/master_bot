from telebot import types

reg = types.InlineKeyboardMarkup()
reg.row(types.InlineKeyboardButton("Зарегистрироваться✅", callback_data="reg"))

admin = types.ReplyKeyboardMarkup(True)
admin.add("Пользователи👤", "Начислить cashback💰")
admin.add("Установить номер📞", "Назначить админа🦸")
admin.add("Обновить Google Doc♻️", "Google Doc link")
admin.add("Сделать рассылку✉️", "Списать балы🙍")
admin.add("Вернуться в меню👨‍💻")

a = '🙊'
profile = types.ReplyKeyboardMarkup(True)
profile.add("Сделать заказ⚙️", "Мой профиль👤")
profile.add("Связаться с мастером🧑‍🔧", "Узнать цену💵")

dostavka = types.ReplyKeyboardMarkup(True)
dostavka.add("Вызвать курьера🏎", "Приеду в мастерскую🔧")
dostavka.add("Вернуться в меню👨‍💻")

delete = types.InlineKeyboardMarkup()
del1 = types.InlineKeyboardButton("❌Закрыть", callback_data="delete")
delete.row(del1)

devices = types.InlineKeyboardMarkup()
phone = types.InlineKeyboardButton("📱Телефон", callback_data="phone")
tablet = types.InlineKeyboardButton("📲Планшет", callback_data="tablet")
laptop = types.InlineKeyboardButton("💻Ноутбук", callback_data="laptop")
tv = types.InlineKeyboardButton("🖥Телевизор", callback_data="tv")
devices.row(phone, tablet)
devices.row(laptop, tv)
devices.row(del1)

choice_brand = types.InlineKeyboardMarkup(row_width=1)
apple = types.InlineKeyboardButton("Apple", callback_data="apple")
huawei_honor = types.InlineKeyboardButton("Huawei, Honor", callback_data="huawei_honor")
samsung = types.InlineKeyboardButton("Samsung", callback_data="samsung")
xiaomi = types.InlineKeyboardButton("Xiaomi", callback_data="xiaomi")
oppo = types.InlineKeyboardButton("Oppo", callback_data="oppo")
realmi = types.InlineKeyboardButton("Realmi", callback_data="realmi")
vivo = types.InlineKeyboardButton("Vivo", callback_data="vivo")
choice_brand.add(apple, huawei_honor, samsung, xiaomi, oppo, realmi, vivo, del1)

apple_buttons = types.InlineKeyboardMarkup(row_width=3)
apple_b1 = types.InlineKeyboardButton("5/5с/5S/SE", callback_data="iPhone 5/5с/5S/SE")
apple_b2 = types.InlineKeyboardButton(" 6 ", callback_data="iPhone 6")
apple_b3 = types.InlineKeyboardButton(" 6+ ", callback_data="iPhone 6 plus")
apple_b4 = types.InlineKeyboardButton(" 6s ", callback_data="iPhone 6s")
apple_b5 = types.InlineKeyboardButton(" 6s+ ", callback_data="iPhone 6s plus")
apple_b6 = types.InlineKeyboardButton(" 7 ", callback_data="iPhone 7")
apple_b7 = types.InlineKeyboardButton(" 7+ ", callback_data="iPhone 7 plus")
apple_b8 = types.InlineKeyboardButton(" 8 ", callback_data="iPhone 8")
apple_b9 = types.InlineKeyboardButton(" 8+ ", callback_data="iPhone 8 plus")
apple_b10 = types.InlineKeyboardButton(" X ", callback_data="iPhone X")
apple_b11 = types.InlineKeyboardButton(" XS ", callback_data="iPhone XS")
apple_b12 = types.InlineKeyboardButton("XS MAX", callback_data="iPhone XS MAX")
apple_b13 = types.InlineKeyboardButton(" 11 ", callback_data="iPhone 11")
apple_b14 = types.InlineKeyboardButton("11 Pro", callback_data="iPhone 11 Pro")
apple_b15 = types.InlineKeyboardButton("11 Pro Max", callback_data="iPhone 11 Pro Max")
apple_b16 = types.InlineKeyboardButton(" XR ", callback_data="iPhone XR")
apple_b17 = types.InlineKeyboardButton("SE 2020", callback_data="iPhone SE 2020")
apple_b18 = types.InlineKeyboardButton("12 mini", callback_data="iPhone 12 mini")
apple_b19 = types.InlineKeyboardButton(" 12 ", callback_data="iPhone 12")
apple_b20 = types.InlineKeyboardButton("12 Pro", callback_data="iPhone 12 Pro")
apple_b21 = types.InlineKeyboardButton("12 Pro Max", callback_data="iPhone 12 Pro Max")
apple_b22 = types.InlineKeyboardButton("13 mini", callback_data="iPhone 13 mini")
apple_b23 = types.InlineKeyboardButton(" 13 ", callback_data="iPhone 13")
apple_b24 = types.InlineKeyboardButton(" 13 Pro", callback_data="iPhone 13 Pro")
apple_b25 = types.InlineKeyboardButton("13 Pro Max", callback_data="iPhone 13 Pro Max")
apple_b26 = types.InlineKeyboardButton("watch", callback_data="watch")
apple_b27 = types.InlineKeyboardButton("ipad", callback_data="ipad")
apple_buttons.add(apple_b1, apple_b2, apple_b3, apple_b4, apple_b5, apple_b6, apple_b7, apple_b8, apple_b9, apple_b10,
                  apple_b11, apple_b12, apple_b13, apple_b14, apple_b15, apple_b16, apple_b17, apple_b18, apple_b19,
                  apple_b20, apple_b21, apple_b22, apple_b23, apple_b24, apple_b25, apple_b26, apple_b27)
apple_buttons.row(del1)

huawei_buttons = types.InlineKeyboardMarkup(row_width=1)
hu_b1 = types.InlineKeyboardButton("7A/Y5 Prime 2018/9s/Y5p", callback_data="Honor 7A")
hu_b2 = types.InlineKeyboardButton("8/8 Lite/P8 Lite 2017", callback_data="Honor 8 Lite")
hu_b3 = types.InlineKeyboardButton("8A/8A Pro/8A Prime", callback_data="Honor 8A")
hu_b4 = types.InlineKeyboardButton("9/9A/Y6p/9 Lite", callback_data="Honor 9A")
hu_b5 = types.InlineKeyboardButton("10 Lite/10i/20i/10X Lite/P Smart 2021", callback_data="Honor 10 Lite")
hu_b6 = types.InlineKeyboardButton("20 lite/20/20 Pro/Nova 5T", callback_data="Honor 20 Lite")
hu_b7 = types.InlineKeyboardButton("Mate 10/Mate 10 Pro", callback_data="Huawei Mate 10 Pro")
hu_b8 = types.InlineKeyboardButton("Nova/Mate10Lite/Nova2i/Mate20/Mate20Lite", callback_data="Huawei Mate 10 Lite")
hu_b9 = types.InlineKeyboardButton("Nova 2/Nova 2 Plus", callback_data="Huawei Nova 2 Plus")
hu_b10 = types.InlineKeyboardButton("Nova 3", callback_data="Huawei Nova 3")
hu_b11 = types.InlineKeyboardButton("P9 Lite", callback_data="Huawei P9 Lite")
hu_b12 = types.InlineKeyboardButton("P10 Lite", callback_data="Huawei P10 Lite")
hu_b13 = types.InlineKeyboardButton("P30/P30 Lite/20S", callback_data="Huawei P30")
hu_b14 = types.InlineKeyboardButton("P40 Lite E/9C/Y7p/P40 Lite/Nova 6 SE", callback_data="Huawei P40 Lite")
hu_b15 = types.InlineKeyboardButton("P Smart Z/9X/P Smart 2019/P Smart", callback_data="Huawei P Smart")
hu_b16 = types.InlineKeyboardButton("Y6 2019/Y6 Prime 2019/Y6 Pro 2019/Y6s", callback_data="Huawei Y6 Prime")
hu_b17 = types.InlineKeyboardButton("7A Pro/7C/Y6 Prime 2018", callback_data="Honor 7C")
hu_b18 = types.InlineKeyboardButton("8 Pro/8C/8X", callback_data="Honor 8 Pro")

huawei_buttons.add(hu_b1, hu_b2, hu_b3, hu_b4, hu_b5, hu_b6, hu_b7, hu_b8, hu_b9)
huawei_buttons.row(hu_b10, hu_b11, hu_b12)
huawei_buttons.row(hu_b12, hu_b13)
huawei_buttons.add(hu_b14, hu_b15, hu_b16, hu_b17, hu_b18)
huawei_buttons.row(del1)

samsung_buttons = types.InlineKeyboardMarkup(row_width=4)
s_b1 = types.InlineKeyboardButton("A3", callback_data="SAMSUNG A3")
s_b2 = types.InlineKeyboardButton("A5", callback_data="SAMSUNG A5")
s_b3 = types.InlineKeyboardButton("A6", callback_data="SAMSUNG A6")
s_b4 = types.InlineKeyboardButton("A7", callback_data="SAMSUNG A7")
s_b5 = types.InlineKeyboardButton("A8", callback_data="SAMSUNG A8")
s_b6 = types.InlineKeyboardButton("A9", callback_data="SAMSUNG A9")
s_b7 = types.InlineKeyboardButton("A10/M10", callback_data="SAMSUNG A10")
s_b8 = types.InlineKeyboardButton("A10s", callback_data="SAMSUNG A10s")
s_b9 = types.InlineKeyboardButton("A20/A30s/M10s", callback_data="SAMSUNG A30s")
s_b10 = types.InlineKeyboardButton("A20s", callback_data="SAMSUNG A20s")
s_b11 = types.InlineKeyboardButton("A21s", callback_data="SAMSUNG A21s")
s_b12 = types.InlineKeyboardButton("A30/A50/50s/A50s/M30", callback_data="SAMSUNG A50s")
s_b13 = types.InlineKeyboardButton("A31", callback_data="SAMSUNG A31")
s_b14 = types.InlineKeyboardButton("A40/A40s", callback_data="SAMSUNG A40")
s_b15 = types.InlineKeyboardButton("A41", callback_data="SAMSUNG A41")
s_b16 = types.InlineKeyboardButton("A51", callback_data="SAMSUNG A51")
s_b17 = types.InlineKeyboardButton("A70", callback_data="SAMSUNG A70")
s_b18 = types.InlineKeyboardButton("A71/Note 10 Lite/S10 Lite", callback_data="SAMSUNG A71")
s_b19 = types.InlineKeyboardButton("A80", callback_data="SAMSUNG A80")
s_b20 = types.InlineKeyboardButton("J2", callback_data="SAMSUNG J2")
s_b21 = types.InlineKeyboardButton("J3", callback_data="SAMSUNG J3")
s_b22 = types.InlineKeyboardButton("J4/J4 Plus/J6 Plus", callback_data="SAMSUNG J4")
s_b23 = types.InlineKeyboardButton("J5", callback_data="SAMSUNG J5")
s_b24 = types.InlineKeyboardButton("J6", callback_data="SAMSUNG J6 2018")
s_b25 = types.InlineKeyboardButton("J7", callback_data="SAMSUNG J7")
s_b26 = types.InlineKeyboardButton("J8", callback_data="SAMSUNG J8")
samsung_buttons.add(s_b1, s_b2, s_b3, s_b4, s_b5, s_b6, s_b7, s_b8, s_b10, s_b11, s_b13, s_b14, s_b15,
                    s_b16, s_b17, s_b19, s_b20, s_b21, s_b23, s_b24)
samsung_buttons.row(s_b25, s_b9)
samsung_buttons.row(s_b12)
samsung_buttons.row(s_b18)
samsung_buttons.row(s_b22)
samsung_buttons.row(del1)

xiaomi_buttons = types.InlineKeyboardMarkup(row_width=1)
x_b1 = types.InlineKeyboardButton("Mi 6/6c", callback_data="Xiaomi Mi 6")
x_b2 = types.InlineKeyboardButton("Mi 8/8 Pro/8 SE/8 lite", callback_data="Xiaomi Mi 8 pro")
x_b3 = types.InlineKeyboardButton("Mi9/9SE/9Lite/A3Lite/CC9/9T/9TPro/K20/K20Pro", callback_data="Xiaomi Mi 9 SE")
x_b4 = types.InlineKeyboardButton("Mi A1", callback_data="Xiaomi Mi A1")
x_b5 = types.InlineKeyboardButton("Mi A2/6x", callback_data="Xiaomi Mi A2")
x_b6 = types.InlineKeyboardButton("Mi A2 lite/Redmi 6 Pro", callback_data="Xiaomi Redmi 6 Pro")
x_b7 = types.InlineKeyboardButton("Mi A3/CC9e", callback_data="Xiaomi Mi CC9e")
x_b8 = types.InlineKeyboardButton("Pocophone F1", callback_data="Xiaomi Pocophone F1")
x_b9 = types.InlineKeyboardButton("Redmi 3/3pro/3s/3x/Note3/Note3Pro/Note3ProSE", callback_data="Xiaomi Redmi 3 pro")
x_b10 = types.InlineKeyboardButton("Redmi 4a/4x/Note 4x", callback_data="Xiaomi Redmi 4x")
x_b11 = types.InlineKeyboardButton("Redmi 5/5a/5 plus/Note 5/Note 5a", callback_data="Xiaomi Redmi 5")
x_b12 = types.InlineKeyboardButton("Redmi 6/6A/Note 6 pro", callback_data="Xiaomi Redmi 6a")
x_b13 = types.InlineKeyboardButton("Redmi 7/7A/Note 7/Note 7 pro", callback_data="Xiaomi Redmi 7")
x_b14 = types.InlineKeyboardButton("Redmi 8/8a/Note 8/Note 8 pro/Note 8 T", callback_data="Xiaomi Redmi 8")
x_b15 = types.InlineKeyboardButton("Redmi 9/Note 9/Note 9s/Note 9 Pro", callback_data="Xiaomi Redmi 9")
x_b16 = types.InlineKeyboardButton("Redmi 9a/9c", callback_data="Xiaomi Redmi 9a")
xiaomi_buttons.add(x_b1, x_b2, x_b3)
xiaomi_buttons.row(x_b4, x_b5)
xiaomi_buttons.add(x_b6, x_b7, x_b8, x_b9, x_b10, x_b11, x_b12, x_b13, x_b14, x_b15, x_b16)
xiaomi_buttons.row(del1)
