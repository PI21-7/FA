from aiogram.types.base import String

import Buttons
import transliterate as tr
import aiogram.utils.exceptions

from Utils.utils import *
from config import *

from datetime import datetime
from aiogram.utils import executor
from Utils.date import week_definition
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda query: 'Inline' not in query.data, state=SelfState.Add_state)
async def add_homework_subject(query: types.CallbackQuery, state: FSMContext) -> object or None:
	"""Выбираем предмет домашнего задания в управлении заданиями"""
	try:
		async with state.proxy() as data:
			data['subject'] = query.conf
			date_count = data['date_count']
			data["state"] = True

		schedule = get_group_schedule(group=get_user_group(query.message), start=week_definition(date_count, debug=True))
		transliterated_schedule = list(map(
			lambda x: tr.translit(x, language_code='ru', reversed=True)[:len(x) // 2 + 1], schedule))
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


@dp.callback_query_handler(lambda query: 'Inline' not in query.data, state=SelfState.Edit_state)
async def add_homework_edit_subject(query: types.CallbackQuery, state: FSMContext) -> None:
	"""Тоже самое что и сверху, только для редактирования"""
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
		await bot.edit_message_text(
			chat_id=query.message.chat.id,
			message_id=query.message.message_id,
			text=f'*Введите новое задание*',
			parse_mode='markdown')
	except KeyError as e:
		print(e)


@dp.message_handler(commands=['start'], state="*")
async def process_start_command(message: types.Message, wrong: bool = False):
	"""Обработка /start и регистрация пользователя"""
	msg = "Привет! Для получения задания, скажи из какой ты группы!\n\nНапример: ПИ21-7" if not wrong \
		else 'Введи ещё раз свою группу\n\n*Например: ПИ20-4*'
	await message.answer(msg, parse_mode='markdown')
	await SelfState.Group_state.set()


@dp.message_handler(state=SelfState.Group_state)
async def group_state_command(message: types.Message, state: FSMContext):
	"""Регистрация группы пользователя и добавление в БД"""
	await state.finish()
	chat_id = message.chat.id
	user_group = message.text.upper()
	if user_group.replace('-', '').isalnum() and '-' in user_group:
		await message.answer("Нажми на кнопку, чтобы получить домашнее задание.", reply_markup=Buttons.answer_start)
		UDB.add_user(chat_id=chat_id, user_group=user_group)
	else:
		await message.answer("Мы не знаем такой группы)")
		await process_start_command(message, wrong=True)


@dp.message_handler(lambda message: message.text == 'Управление заданиями', state="*")
async def process_add_command(message: types.Message, state: FSMContext):
	"""Обработка управления заданиями"""
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
			text="*Вы не можете управлять заданиями, для получения возможности → @Nps_rf или @monotank*",
			parse_mode='markdown')


@dp.callback_query_handler(text='Inline_Add')
async def add_homework_state(call: types.CallbackQuery):
	"""Стадия выбора предмета домашнего задания"""
	start_date = datetime.now()
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
	"""Стадия добавления самого дз"""
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
	Exercise: String = text
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
async def edit_init(call: types.CallbackQuery, state: FSMContext):
	"""Обработка Инлайна редактирования"""
	async with state.proxy() as data:
		data['state'] = True
		date_count = data['date_count']
	start_date, end_date = week_definition(date_count)
	await bot.edit_message_text(
		chat_id=call.message.chat.id,
		message_id=call.message.message_id,
		text=f"*На какой день задание?\n📅 {start_date} - {end_date} 📅*",
		reply_markup=Buttons.Inline_Date_ADD,
		parse_mode="markdown"
	)
	await SelfState.Edit_state.set()


@dp.message_handler(state=SelfState.Edit_state)
async def edit_homework(message: types.Message, state: FSMContext):
	"""Редактирование записей и запросы к БД"""
	text = message.text
	async with state.proxy() as data:
		Date = data['date']
		Subject = data['subject']
	if HDB.is_exists(date=Date, subject_name=Subject, group=get_user_group(message)):
		HDB.delete_homework(subject_name=Subject, date=Date, group=get_user_group(message))
		ADD_STATE = HDB.add_homework(
			subject_name=Subject,
			username=message.from_user.username,
			text=text, date=Date,
			group=get_user_group(message),
			edit=True)
		await message.answer(
			text=f'*{ADD_STATE}*', parse_mode='markdown')
		await state.finish()
	else:
		await message.answer(text='*Такой записи не существует!*', parse_mode='markdown')
		await state.finish()


@dp.callback_query_handler(lambda query: query.data.split('_')[2][0] == 'B', state=SelfState.Add_state)
async def add_homework_date(query: types.CallbackQuery, state: FSMContext):
	"""Выбор даты домашнего задания в состоянии добавления домашнего задания"""
	async with state.proxy() as data:
		current_state = data['state']
		date_count = data['date_count']
	if current_state:
		day = query.data.split("_")[2]
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


@dp.callback_query_handler(lambda query: query.data.split('_')[2][0] == 'B', state=SelfState.Edit_state)
async def add_homework_date(query: types.CallbackQuery, state: FSMContext):
	"""Тоже самое только для редактирования домашнего задания"""
	async with state.proxy() as data:
		current_state = data['state']
		date_count = data['date_count']
	if current_state:
		day = query.data.split("_")[2]
		start_date = week_definition(date_count, debug=True)
		async with state.proxy() as data:
			data['date'] = (start_date + timedelta(days=days[day])).strftime('%d.%m.%Y')
			Date = data["date"]
		homework = HDB.is_available_homework_by_date(date=Date, group=get_user_group(query.message), data=True)
		homework = list(map(lambda x: x[0], homework))
		print(homework)
		await bot.edit_message_text(
			text='*Выберите предмет*',
			chat_id=query.message.chat.id,
			message_id=query.message.message_id,
			parse_mode='markdown',
			reply_markup=Buttons.create_subjects_keyboard(homework)
		)
		await SelfState.Edit_state.set()


@dp.callback_query_handler(lambda query: query.data.split('_')[2][0] == 'B')
async def homework_reply(query: types.CallbackQuery, state: FSMContext):
	"""Получение домашнего задания, запросы к БД и выдача"""
	day = query.data.split("_")[2]
	try:
		async with state.proxy() as data:
			date_count = data['date_count']
		start_date = week_definition(date_count, debug=True)
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
				__text += f'{str(num + 1)}) ' + subject[0] + ': ' + subject[1] + '\n'
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
	"""Обработка выбора <Получить задание!>, вызов меню с выбором даты"""
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
	"""Обработка Инлайна на выдачу всего домашнего задания на неделю"""
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
					f'{str(num + 1)}) ' + subject[0] + ': ' + subject[1] + '\n'
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
	"""Обработка листания выбора даты ВНИЗ"""
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
	"""Обработка листания выбора даты ВВЕРХ"""
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
