from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili
CHANNELS = env.list("CHANNELS")

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")

FREE_TRIAL_PERIOD = 5
CARD_NUMBER = "9860 1766 0132 6737"
AMOUNT_PER_MONTH_IN_WORD = "qirq to'qqiz ming so'm"
AMOUNT_PER_MONTH = "49 000"
