from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

markup = ReplyKeyboardMarkup(resize_keyboard=True)
btn_1 = KeyboardButton("Головне меню 🏠")
btn_2 = KeyboardButton("Help 🔔")
markup.add(btn_1).add(btn_2)
