from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

from Course_1.Telegram_Bot.config import TOKEN
from Course_1.Telegram_Bot.db import Database

days_of_week = {
	1: 'Понедельник',
	2: 'Вторник',
	3: 'Среда',
	4: 'Четверг',
	5: 'Пятница',
	6: 'Суббота'
}

days = {
	'Bm': 0,
	'Bt': 1,
	'Bwd': 2,
	'Bth': 3,
	'Bf': 4,
	'BSn': 5
}


class SelfState(StatesGroup):
	Group_state = State()
	Add_state = State()
	Edit_state = State()


storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
HDB, UDB = Database(), Database.UsersDB()
