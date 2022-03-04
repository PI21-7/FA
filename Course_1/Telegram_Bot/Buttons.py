from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


answer_start = ReplyKeyboardMarkup(resize_keyboard=True).add("Получить задание!")
Inline_Date = InlineKeyboardMarkup(inline_keyboard=True, row_width=3)
Inline_Date_Bm = InlineKeyboardButton(text='понедельник 💀', callback_data='Inline_Date_Bm')
Inline_Date_Bt = InlineKeyboardButton(text='Вторник 🤯', callback_data='Inline_Date_Bt')
Inline_Date_Bwd = InlineKeyboardButton(text='Среда 😒', callback_data='Inline_Date_Bwd')
Inline_Date_Bth = InlineKeyboardButton(text='Четверг 🤨', callback_data='Inline_Date_Bth')
Inline_Date_Bf = InlineKeyboardButton(text='Пятница 🍺', callback_data='Inline_Date_Bf')
Inline_Date_Sn = InlineKeyboardButton(text='Суббота 😎', callback_data='Inline_Date_Sn')
Inline_Date_Down = InlineKeyboardButton(text='⏬', callback_data='Inline_Date_Down')


Inline_Date.add(Inline_Date_Bm).add(Inline_Date_Bt).add(Inline_Date_Bwd).add(Inline_Date_Bth).add(Inline_Date_Bf)\
    .add(Inline_Date_Sn).add(Inline_Date_Down)
