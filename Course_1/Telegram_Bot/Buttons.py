from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


answer_start = ReplyKeyboardMarkup(resize_keyboard=True).add("Получить задание!").add('Управление заданиями')
Inline_Date = InlineKeyboardMarkup(inline_keyboard=True, row_width=3)
Inline_Date_Week = InlineKeyboardButton(text='Вся неделя 🥶', callback_data='Inline_Date_Week')
Inline_Date_Bm = InlineKeyboardButton(text='понедельник 💀', callback_data='Inline_Date_Bm')
Inline_Date_Bt = InlineKeyboardButton(text='Вторник 🤯', callback_data='Inline_Date_Bt')
Inline_Date_Bwd = InlineKeyboardButton(text='Среда 😒', callback_data='Inline_Date_Bwd')
Inline_Date_Bth = InlineKeyboardButton(text='Четверг 🤨', callback_data='Inline_Date_Bth')
Inline_Date_Bf = InlineKeyboardButton(text='Пятница 🍺', callback_data='Inline_Date_Bf')
Inline_Date_Sn = InlineKeyboardButton(text='Суббота 😎', callback_data='Inline_Date_BSn')
Inline_Date_Down = InlineKeyboardButton(text='⏬', callback_data='Inline_Date_Down')
Inline_Date_Up = InlineKeyboardButton(text='⏫', callback_data='Inline_Date_Up')
Inline_Manage = InlineKeyboardMarkup(inline_keyboard=True)
Inline_Edit = InlineKeyboardButton(text='Редактировать ДЗ', callback_data='Inline_Edit')
Inline_Add = InlineKeyboardButton(text='Добавить ДЗ', callback_data='Inline_Add')
Inline_Manage.add(Inline_Edit).add(Inline_Add)


Inline_Date.add(Inline_Date_Up).add(Inline_Date_Week).add(Inline_Date_Bm).add(Inline_Date_Bt).add(Inline_Date_Bwd)\
    .add(Inline_Date_Bth).add(Inline_Date_Bf)\
    .add(Inline_Date_Sn).add(Inline_Date_Down)
