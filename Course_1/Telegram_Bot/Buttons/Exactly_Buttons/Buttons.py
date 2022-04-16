from typing import Iterable

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from transliterate import translit


def __compose_str(string):
    if len(string) < 22:
        return string
    return string[len(string) // 2:]


def create_subjects_keyboard(array: Iterable):
    buttons_list = []
    for item in array:
        buttons_list.append([InlineKeyboardButton(text=item, callback_data=translit(
            __compose_str(item), language_code='ru', reversed=True))])
    keyboard_inline_buttons = InlineKeyboardMarkup(inline_keyboard=buttons_list)
    return keyboard_inline_buttons


def create_faculties_keyboard(array: Iterable):
    buttons_list = []
    for item in array:
        item: str
        buttons_list.append([InlineKeyboardButton(text=item, callback_data=translit(
            __compose_str(item), language_code='ru', reversed=True))])
    keyboard_inline_buttons = InlineKeyboardMarkup(inline_keyboard=buttons_list)
    return keyboard_inline_buttons


answer_start = ReplyKeyboardMarkup(resize_keyboard=True).add("Получить задание!").add('Управление заданиями').add('Полезные материалы')
Inline_Date = InlineKeyboardMarkup(inline_keyboard=True, row_width=3)
Inline_Date_Week = InlineKeyboardButton(text='Вся неделя 🥶', callback_data='Inline_Date_Week')
Inline_Date_Bm = InlineKeyboardButton(text='Понедельник 💀', callback_data='Inline_Date_Bm')
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
Inline_Delete = InlineKeyboardButton(text='Удалить ДЗ', callback_data='Inline_Delete')
Inline_Materials = InlineKeyboardButton(text='Добавить материалы', callback_data='Inline_Materials')
Inline_Manage_Materials = InlineKeyboardButton(text='Управление материалами', callback_data='Inline_Manage_Materials')
Inline_Manage.add(Inline_Add).add(Inline_Edit).add(Inline_Delete).add(Inline_Materials)

Inline_Date_ADD = InlineKeyboardMarkup()

Inline_Date_ADD.add(Inline_Date_Up).add(Inline_Date_Bm).add(Inline_Date_Bt).add(Inline_Date_Bwd)\
    .add(Inline_Date_Bth).add(Inline_Date_Bf)\
    .add(Inline_Date_Sn).add(Inline_Date_Down)

Inline_Date.add(Inline_Date_Up).add(Inline_Date_Week).add(Inline_Date_Bm).add(Inline_Date_Bt).add(Inline_Date_Bwd)\
    .add(Inline_Date_Bth).add(Inline_Date_Bf)\
    .add(Inline_Date_Sn).add(Inline_Date_Down)

Inline_Question_Why = InlineKeyboardButton(
    text='А почему это может быть мне полезным?',
    callback_data='Inline_Question_Why')
Inline_About_Questions = InlineKeyboardMarkup()
Inline_About_Questions.add(Inline_Question_Why)



