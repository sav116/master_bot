from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

token = env.str("BOT_TOKEN")  # Забираем значение типа str

chat = "-1001244336776" # test master bot
coder = "292721851" # Artem S
admins = [1742008095, 819730005, 268018242, 292721851, 287981918]
delivery = {}
cura = ["Вызвать курьера🏎"]

sam = ["Приеду в мастерскую🔧"]
