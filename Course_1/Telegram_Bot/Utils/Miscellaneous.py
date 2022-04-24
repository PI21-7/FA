import sys

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

from Utils.Schedule import *
from config import *
from Database import Database


sys.path.append("..")


class SelfState(StatesGroup):
	Faculty_state 			= State()
	Group_state 			= State()
	Groups_state 			= State()
	Add_state 				= State()
	Edit_state 				= State()
	Delete_state 			= State()
	Parse_state 			= State()
	Materials_state 		= State()
	Materials_parse_state 	= State()
	Manual_input_state 		= State()
	Delete_materials_state 	= State()


storage 	= MemoryStorage()
bot 		= Bot(token=TOKEN)
admin_bot 	= Bot(token=ADMIN_BOT_TOKEN)
dp 			= Dispatcher(bot, storage=storage)
HDB 		= Database()

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


def get_user_group(message: types.Message):
	return HDB.get_user_group(chat_id=message.chat.id)[0][0]


def get_group_schedule(group: str, start) -> list:
	end = (start + timedelta(weeks=2)).strftime("%Y.%m.%d")
	start = start.strftime("%Y.%m.%d")
	schedule = Schedule.get_group_schedule(group=group, start=start, end=end)
	lessons = set()
	for i in schedule:
		if i['discipline'] == 'Элективные дисциплины по физической культуре и спорту':
			continue
		lessons.add(
			i['discipline'] + ' ' + i['lecturer_title'].split()[0]
			if i['discipline'] == 'Иностранный язык'
			else i['discipline'])

	return list(lessons)


def green_list(path: str = 'Admin/admins.txt'):
	with open(path, 'r+', encoding='utf-8') as data:
		return list(filter(lambda x: '\n' not in x, data.readline().split(',')))


