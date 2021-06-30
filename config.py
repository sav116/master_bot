from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

token = env.str("BOT_TOKEN")  # Забираем значение типа str
admins = env.list("ADMINS")  # Тут у нас будет список из админов

chat = "-1001586497619"
coder = "1742008095"

delivery = {}
cura = ["Вызвать курьера🏎"]

sam = ["Приеду в мастерскую🔧"]



iphone5 = ["iphone 5", "iphone 5c", "iphone 5s", "iphone se", "айфон 5", "айфон 5ц", "айфон 5 се", "айфон 5s", "айфон 5se"]

iphone6 = ["iphone 6", "iphone6", "айфон 6","айфон6"]

iphone6Plus = ["iphone 6+", "iphone6+", "iphone 6 +", "айфон 6+", "айфон 6 +", "айфон 6 плюс", "iphone 6 plus"]

iphone6s = ["iphone6s", "iphone 6s", "iphone6 s", "айфон 6с", "айфон 6s"]

iphone6sPlus = ["iphone6s+", "iphone 6s+", "iphone 6s +", "айфон 6 с+","айфон 6 s+", "айфон 6 с плюс", "iphone 6 s plus"]

iphone7 = ["iphone 7", "iphone7", "айфон 7", "айфон7"]

iphone7Plus = ["iphone7+", "iphone 7+", "iphone7 +", "iphone 7 +", "айфон 7+", "айфон 7 плюс", "iphone 7 plus"]

iphone8 = ["iphone8", "iphone 8"]

iphone8Plus = ["iphone8+", "iphone 8+", "iphone8 +", "iphone 8 +", "айфон 8 +", "айфон 8+", "айфон 8 плюс", "iphone 8 plus"]

iphoneX = ["iphonex", "iphone x", "iphone10", "iphone 10", "айфон 10","айфон х", "айфон x"]

iphoneXS = ["iphonexs", "iphone xs", "iphone10s", "iphone 10s", "айфон 10с","айфон 10 с","айфон xs"]

iPhoneXSMAX = ["iphonexsmax", "iphonexs max", "iphone xs max","айфон 10 макс","айфон 10 max","айфон xs max"]

iPhone11 = ["iphone 11", "iphone11", "айфон 11"]

iPhone11Pro = ["iphone 11 pro", "iphone11pro", "iphone11 pro", "iphone 11pro", "айфон 11 про", "айфон 11про"]

iPhone11ProMax = ["iphone 11 pro max", "iphone11 pro max", "iphone11promax", "iphone 11pro max", "iphone 11 promax", "айфон 11 про макс"]

iPhoneXR = ["iphone xr", "iphonexr", "iphone 10r", "iphone10r", "айфон 10р", "айфон 10r", "айфон xr"]

watch = ["apple watch", "applewatch", "епл вотч", "эпл вотч", "епл воч", "эпл воч", "часы"]

samsungA10 = ["samsung a10", "samsunga10", "samsung a 10", "самсунг a10"]

samsungA10s = ["samsung a10s", "samsunga10s", "samsung a 10s", "самсунг a10s", "самсунг a10 c"]

samsungA20 = ["samsung a20", "samsunga20", "samsung a 20", "самсунг a20"]

samsungA20s = ["samsung a20s", "samsunga20s", "samsung a 20s", "самсунг a20 c"]


samsungA21s = ["samsung a21s", "samsunga21s", "samsung a 21s", "самсунг a21 c"]

samsungA3 = ["samsung a3", "samsunga3", "samsung a 3", "самсунг a3"]

samsungA30 = ["samsung a30", "samsunga30", "samsung a 30", "самсунг a30", "samsung a305f", "самсунг а305ф", "самсунг а305f", "samsung a50", "самсунг а50", "samsung a505f", "самсунг а505ф",
"самсунг а505f", "samsung a50s", "самсунг a50s", "самсунг a507", "samsung a507", "samsung m30", "самсунг м30", "самсунг m30"]

samsungA31 = ["samsung a31", "samsunga31", "samsung a 31", "самсунг a31", "samsung a315f", "самсунг а315ф", "самсунг а315f"]

samsungA40 = ["samsung a40", "samsunga40", "samsung a 40", "самсунг a40", "samsung a40s", "samsunga40s", "samsung a 40s", "самсунг a40s", "samsung a405f", "самсунг а405ф", "самсунг а405f"]

samsungA41 = ["samsung a41", "samsunga41", "samsung a 41", "самсунг a41"]

samsungA5 = ["samsung a5", "samsunga5", "samsung a 5", "самсунг a5"]

samsungA51 = ["samsung a51", "samsunga51", "samsung a 51", "самсунг a51"]

samsungA6 = ["samsung a6", "samsunga6", "samsung a 6", "самсунг a6","samsung a6+", "samsunga6+", "samsung a 6+", "самсунг a6+", "samsung a6 plus", "samsunga6plus", "samsung a 6plus", "самсунг a6 плюс"]

samsungA7 = ["samsung a7", "samsunga7", "samsung a 7", "самсунг a7"]

samsungA70 = ["samsung a70", "samsunga70", "samsung a 70", "самсунг a70"]

samsungA71 = ["samsung a71", "samsunga71", "samsung a 71", "самсунг a71", "samsung a715f", "самсунг а715f", "samsung note 10 lite", "samsung s10 lite", "samsung g770f"]

samsungA8 = ["samsung a8", "samsunga8", "samsung a 8", "самсунг a8","samsung a8+", "samsunga8+", "samsung a 8+", "самсунг a8+", "samsung a8 plus", "samsunga8plus", "samsung a 8plus", "самсунг a8 плюс"]

samsungA80 = ["samsung a80", "samsunga80", "samsung a 80", "самсунг a80"]

samsungA9 = ["samsung a9", "samsunga9", "samsung a 9", "самсунг a9"]








