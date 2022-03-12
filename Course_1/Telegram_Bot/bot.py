import datetime
from datetime import timedelta

from Schedule import Schedule
import transliterate as tr
import aiogram.utils.exceptions
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import *
import Buttons
from db import Database
from date import week_definition
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class SelfState(StatesGroup):
	Group_state = State()
	Add_state = State()
	Edit_state = State()


storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
HDB = Database()
UDB = Database.UsersDB()
days_of_week = {
	1: 'Понедельник',
	2: 'Вторник',
	3: 'Среда',
	4: 'Четверг',
	5: 'Пятница',
	6: 'Суббота'
}


def get_user_group(message: types.Message):
	return UDB.get_user_group(chat_id=message.chat.id)[0][0]


def get_group_schedule(group: str, start: datetime.date) -> list:
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


@dp.callback_query_handler(lambda query: 'Inline' not in query.data, state=SelfState.Add_state)
async def add_homework_subject(query: types.CallbackQuery, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['subject'] = query.conf
			date_count = data['date_count']
			data["state"] = True

		schedule = get_group_schedule(group=get_user_group(query.message), start=week_definition(date_count, debug=True))
		transliterated_schedule = list(map(
			lambda x: tr.translit(x, language_code='ru', reversed=True), schedule))
		subject = None
		for pos, let in enumerate(transliterated_schedule):
			if query.data == let:
				subject = schedule[pos]
		if subject is None:
			async with state.proxy() as data:
				subject = data['subject']

		async with state.proxy() as data:
			data['subject'] = subject
		start_date, end_date = week_definition(date_count)
		await bot.edit_message_text(
			chat_id=query.message.chat.id,
			message_id=query.message.message_id,
			text=f'*На какой день задание?\n📅 {start_date} - {end_date} 📅*',
			reply_markup=Buttons.Inline_Date_ADD,
			parse_mode='markdown')
	except KeyError as e:
		print(e)


@dp.message_handler(commands=['start'], state="*")
async def process_start_command(message: types.Message):
	await message.answer("Привет! Для получения задания, скажи из какой ты группы!\n\nНапример: ПИ21-7")
	await SelfState.Group_state.set()


@dp.message_handler(state=SelfState.Group_state)
async def group_state_command(message: types.Message, state: FSMContext):
	await state.finish()
	await message.answer("Нажми на кнопку, чтобы получить домашнее задание.", reply_markup=Buttons.answer_start)
	chat_id = message.chat.id
	user_group = message.text
	UDB.add_user(chat_id=chat_id, user_group=user_group)


@dp.message_handler(lambda message: message.text == 'Управление заданиями', state="*")
async def process_add_command(message: types.Message, state: FSMContext):
	await state.finish()
	async with state.proxy() as data:
		data['date_count'] = 0
	print(message.from_user.username, 'управляет заданиями')
	if message.from_user.username in green_list:
		await message.answer(
			text='*Что будем делать?*',
			parse_mode='markdown',
			reply_markup=Buttons.Inline_Manage
		)

	else:
		await message.answer(
			text='*Вы не можете управлять заданиями, для получения возможности → @Nps_rf или @monotank*',
			parse_mode='markdown')


@dp.callback_query_handler(text='Inline_Add')
async def add_homework_state(call: types.CallbackQuery):
	start_date = datetime.datetime.now()
	await SelfState.Add_state.set()
	await bot.edit_message_text(
		chat_id=call.message.chat.id,
		message_id=call.message.message_id,
		text=f"*Выберите предмет*",
		parse_mode="markdown",
		reply_markup=Buttons.create_subjects_keyboard(get_group_schedule(get_user_group(call.message), start=start_date))
	)


@dp.message_handler(state=SelfState.Add_state)
async def add_homework(message: types.Message, state: FSMContext):
	text = message.text
	print(message.from_user.username, 'добавил:\n', text)
	try:
		async with state.proxy() as data:
			Date = data['date']
			Subject = data['subject']
			data['state'] = False
	except KeyError:
		await message.answer(text='Ну ладно 🥺', parse_mode='markdown')
		await state.finish()
		return
	await state.finish()
	Exercise = text
	await message.answer(
		text='*{}*'.format(
			HDB.add_homework(
				subject_name=Subject,
				date=Date,
				text=Exercise,
				username=message.from_user.username,
				group=get_user_group(message))),
		parse_mode='markdown')
	try:
		await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
	except aiogram.utils.exceptions.MessageToDeleteNotFound:
		print('Какое-то сообщение не удаляется(')


@dp.callback_query_handler(text='Inline_Edit')
async def edit_init(call: types.CallbackQuery):
	await SelfState.Edit_state.set()
	await bot.edit_message_text(
		chat_id=call.message.chat.id,
		message_id=call.message.message_id,
		text=f"*Введите предмет и дату для редактирования:\n\nПример:* `Алгебра 15.03.2022`",
		parse_mode="markdown",
	)


@dp.message_handler(state=SelfState.Edit_state)
async def edit_homework(message: types.Message, state: FSMContext):
	text = message.text.split()
	if len(text) < 2 or all(map(lambda x: len(x) > 3, text)):
		await message.answer_sticker(sticker='CAACAgIAAxkBAAEEG9BiKojK_SZBFl_KqTqswln3CM1ptQAC7xMAApJeSUuQKkME9nIP_SME')
		await state.finish()
		return 0
	Subject, Date = text[0], text[1]
	if HDB.is_exists(date=Date, subject_name=Subject, group=get_user_group(message)):
		print(message.from_user.username, 'отредактировал:\n', text)
		await bot.edit_message_text(
			chat_id=message.chat.id,
			message_id=message.message_id - 1,
			text=f"*Введите данные для изменения:\n\nПример:* `Алгебра 15.03.2022 Подготовиться к кр`",
			parse_mode="markdown",
		)
		await bot.delete_message(
			chat_id=message.chat.id,
			message_id=message.message_id
		)
		HDB.delete_homework(subject_name=Subject, date=Date, group=get_user_group(message))
		await state.finish()
		await SelfState.Add_state.set()
	else:
		await message.answer(text='*Такой записи не существует!*', parse_mode='markdown')
		await state.finish()


@dp.callback_query_handler(lambda query: query.data.split('_')[2][0] == 'B', state=SelfState.Add_state)
async def add_homework_date(query: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		current_state = data['state']
		date_count = data['date_count']
	if current_state:
		day = query.data.split("_")[2]
		days = {
			'Bm': 0,
			'Bt': 1,
			'Bwd': 2,
			'Bth': 3,
			'Bf': 4,
			'BSn': 5
		}
		start_date = week_definition(date_count, debug=True)
		await bot.edit_message_text(
			text='*Введите домашнее задание*',
			chat_id=query.message.chat.id,
			message_id=query.message.message_id,
			parse_mode='markdown'
		)
		async with state.proxy() as data:
			data['date'] = (start_date + timedelta(days=days[day])).strftime('%d.%m.%Y')
		await SelfState.Add_state.set()


@dp.callback_query_handler(lambda query: query.data.split('_')[2][0] == 'B')
async def homework_reply(query: types.CallbackQuery, state: FSMContext):
	day = query.data.split("_")[2]
	try:
		async with state.proxy() as data:
			date_count = data['date_count']
		start_date = week_definition(date_count, debug=True)
		days = {
			'Bm': 0,
			'Bt': 1,
			'Bwd': 2,
			'Bth': 3,
			'Bf': 4,
			'BSn': 5
		}
		date_to_db = [
			(start_date + timedelta(days=days[day])).strftime('%d.%m.%y'),
			(start_date + timedelta(days=days[day])).strftime('%d.%m.%Y')]

		if HDB.is_available_homework_by_date(
				date=date_to_db[0],
				group=get_user_group(query.message)) or HDB.is_available_homework_by_date(
			date=date_to_db[1],
			group=get_user_group(query.message)):

			date_to_db = date_to_db[0] if HDB.is_available_homework_by_date(
				date=date_to_db[0],
				group=get_user_group(query.message)) else date_to_db[1]

			available_homework = HDB.is_available_homework_by_date(
				date=date_to_db,
				data=True,
				group=get_user_group(query.message))

			__text = str()
			for num, subject in enumerate(available_homework):
				__text += f'{str(num + 1)}) ' + subject[0].capitalize() + ': ' + subject[1] + '\n'
			await query.message.answer(
				text=f'*📅 {days_of_week[days[day] + 1]} {date_to_db}*\n`{__text}`',
				parse_mode='markdown'
			)
			try:
				await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
			except aiogram.utils.exceptions.MessageToDeleteNotFound:
				print('Какое-то сообщение не удаляется(')
		else:
			await query.message.answer(
				text='*Никто не заполнил домашнее задания на этот день* 😭', parse_mode='markdown'
			)

	except KeyError:
		await process_start_command(query.message)


@dp.message_handler(lambda message: message.text == 'Получить задание!',  state="*")
async def process_date(message: types.Message, state: FSMContext):
	print(message.from_user.username, 'получает задание')
	await state.finish()
	async with state.proxy() as data:
		data['date_count'] = 0
		data["state"] = False
	await message.answer(
		f"*Выбираем день недели\n📅 {week_definition(0)[0]} - {week_definition(0)[1]} 📅*",
		parse_mode="markdown", reply_markup=Buttons.Inline_Date)


@dp.callback_query_handler(text='Inline_Date_Week', state='*')
async def all_week_homework(call: types.CallbackQuery, state: FSMContext):
	try:
		async with state.proxy() as data:
			date_count = data['date_count']
		start_date = week_definition(date_count, debug=True)
		for day in range(6):
			current_day = (start_date + timedelta(days=day)).strftime('%d.%m.%Y')
			available_homework = HDB.is_available_homework_by_date(
				date=current_day,
				group=get_user_group(call.message),
				data=True)
			__text = ''

			try:
				await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
			except aiogram.utils.exceptions.MessageToDeleteNotFound:
				print('Какое-то сообщение не удаляется(')

			for num, subject in enumerate(available_homework):
				__text += \
					f'{str(num + 1)}) ' + subject[0].capitalize() + ': ' + subject[1] + '\n'
			if not __text:
				__text = '*Никто не заполнил домашнее задания на этот день* 😭'
			else:
				__text = '`' + __text + '`'
			await call.message.answer(
				text=f'*📅 {days_of_week[day + 1]} {current_day}*\n{__text}',
				parse_mode='markdown')
	except KeyError:
		await process_start_command(call.message)


@dp.callback_query_handler(text="Inline_Date_Down", state='*')
async def callback_down(call: types.CallbackQuery, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['date_count'] += 1
			date_count = data['date_count']
			button_state = data["state"]
			await bot.edit_message_text(
				chat_id=call.message.chat.id,
				message_id=call.message.message_id,
				text=f"*{'Выбираем день недели' if not button_state else 'На какой день задание?'}\n📅 {week_definition(date_count)[0]} - {week_definition(date_count)[1]} 📅*",
				parse_mode="markdown",
				reply_markup=Buttons.Inline_Date_ADD if button_state else Buttons.Inline_Date)

	except KeyError:
		pass


@dp.callback_query_handler(text="Inline_Date_Up", state='*')
async def callback_up(call: types.CallbackQuery, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['date_count'] -= 1
			date_count = data['date_count']
			button_state = data["state"]
		await bot.edit_message_text(
			chat_id=call.message.chat.id,
			message_id=call.message.message_id,
			text=f"*{'Выбираем день недели' if not button_state else 'На какой день задание?'}\n📅 {week_definition(date_count)[0]} - {week_definition(date_count)[1]} 📅*",
			parse_mode="markdown",
			reply_markup=Buttons.Inline_Date_ADD if button_state else Buttons.Inline_Date)
	except KeyError:
		pass


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
