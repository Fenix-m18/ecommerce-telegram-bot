from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
btn_1 = KeyboardButton('Допомога ⭐️')
btn_2 = KeyboardButton('Опис 📌')
btn_3 = KeyboardButton('Каталог 🛒')
btn_4 = KeyboardButton('Адмін 👑')
markup.add(btn_1).insert(btn_2).add(btn_3).insert(btn_4)

only_help_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_1 = KeyboardButton('Допомога ⭐️')
only_help_markup.add(btn_1)
