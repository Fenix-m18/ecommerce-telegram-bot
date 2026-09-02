from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

markup = ReplyKeyboardMarkup(resize_keyboard=True)
btn_1 = KeyboardButton("Головна сторінка 🏠")
btn_2 = KeyboardButton("Help 🔔")
markup.add(btn_1).add(btn_2)
