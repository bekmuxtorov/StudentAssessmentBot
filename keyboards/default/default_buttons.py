from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


phone_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton("☎️ Telefon raqamni ulashish", request_contact=True)
)

main_button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton("🚀 O'quvchilarni baholash"),
    KeyboardButton("📝 Umumiy statistika")
)
