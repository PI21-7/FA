from datetime import timedelta, date

from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

from Course_1.Telegram_Bot.Utils.Schedule import Schedule
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


def get_user_group(message: types.Message) -> "User Group": return UDB.get_user_group(chat_id=message.chat.id)[0][0]


def get_group_schedule(group: str, start: date) -> list:
	"""Получение расписания группы пользователя"""
	end = (start + timedelta(weeks=2)).strftime("%Y.%m.%d")
	start = start.strftime("%Y.%m.%d")
	SCHEDULE = Schedule.get_group_schedule(group=group, start=start, end=end)
	lessons = set()
	for i in SCHEDULE:
		if i['discipline'] == 'Элективные дисциплины по физической культуре и спорту':
			continue
		lessons.add(
			i['discipline'] + ' ' + i['lecturer_title'].split()[0]
			if i['discipline'] == 'Иностранный язык'
			else i['discipline'])

	return list(lessons)
