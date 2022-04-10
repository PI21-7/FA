############################################
import datetime							   #
import transliterate as tr				   #
import aiogram.utils.exceptions			   #
############################################
from Utils.Maintenance import *			   #
from Buttons.Maintenance import *		   #
from Buttons import Buttons				   #
############################################
from datetime import timedelta			   #
from datetime import datetime			   #
from aiogram import types				   #
from aiogram.utils import executor		   #
from Utils.date import week_definition	   #
from aiogram.dispatcher import FSMContext  #
############################################


@dp.message_handler(commands=['start'], state="*")
async def process_start_command(message: types.Message):
	await message.answer("Привет! Для получения задания, скажи из какой ты группы!\n\nНапример: ПИ21-7")
	await SelfState.Group_state.set()


@dp.message_handler(state=SelfState.Parse_state, content_types=types.ContentType.DOCUMENT)
async def parse_attachments(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		date = data['date']
	HDB.attach_file(date=date, filename=message.document.file_id, group=get_user_group(message))


@dp.message_handler(content_types=types.ContentType.DOCUMENT, state=SelfState.Materials_state)
async def process_add_material_command(message: types.Message, state: FSMContext):
	await state.finish()
	await SelfState.Parse_state.set()
	if HDB.is_file_attached_materials(group=get_user_group(message), file_name=message.document.file_name):
		HDB.attach_file_materials(file_id=message.document.file_id, group=get_user_group(message), file_name=message.document.file_name)
		await message.answer("материалы добавлены")
	else:
		await message.answer("этот файл уже добавлен!")


@dp.message_handler(state=SelfState.Materials_state)
async def process_answer_by_document(message: types.Message, state: FSMContext):
	await state.finish()
	await message.answer("Надо было отправить просто файл😭")


@dp.callback_query_handler(text='Inline_Materials')
async def materials_state(call: types.CallbackQuery, _state: FSMContext):
	await bot.send_message(
			chat_id=call.message.chat.id,
			text="Прикрепите материалы",
			parse_mode="markdown"
		)
	await SelfState.Materials_state.set()


@dp.message_handler(lambda message: message.text == 'Полезные материалы',  state="*")
async def process_get_materials(message: types.Message, state: FSMContext):
	await state.finish()
	attachments = HDB.get_attachments_materials(group=get_user_group(message))
	for pos, document in enumerate(attachments):
		await bot.send_document(
			chat_id=message.chat.id,
			document=document[0],
			caption=None,
			parse_mode='markdown')


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
			if query.data in let:
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


@dp.callback_query_handler(lambda query: 'Inline' not in query.data, state=SelfState.Edit_state)
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
			if query.data in let:
				subject = schedule[pos]
				break
		async with state.proxy() as data:
			data['subject'] = subject
		await bot.edit_message_text(
			chat_id=query.message.chat.id,
			message_id=query.message.message_id,
			text=f'*Введите новое задание*',
			parse_mode='markdown')
	except KeyError as e:
		print(e)


@dp.callback_query_handler(text='Inline_Delete')
async def delete_homework_state(query: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		data['state'] = True
		date_count = data['date_count']
		print(data['date_count'])
	start_date, end_date = week_definition(date_count)
	await bot.edit_message_text(
		chat_id=query.message.chat.id,
		message_id=query.message.message_id,
		text=f"*На какой день задание?\n📅 {start_date} - {end_date} 📅*",
		reply_markup=Buttons.Inline_Date_ADD,
		parse_mode="markdown"
	)
	await SelfState.Delete_state.set()


@dp.callback_query_handler(lambda query: 'Inline' not in query.data, state=SelfState.Delete_state)
async def delete_homework(query: types.CallbackQuery, state: FSMContext):
	message = query.message
	async with state.proxy() as data:
		date = data['date']
		date_count = data['date_count']
	schedule = get_group_schedule(group=get_user_group(query.message), start=week_definition(date_count, debug=True))
	transliterated_schedule = list(map(
		lambda x: tr.translit(x, language_code='ru', reversed=True), schedule))
	subject = None
	for pos, let in enumerate(transliterated_schedule):
		if query.data in let:
			subject = schedule[pos]
			break
	group = get_user_group(message)
	print(message.from_user.username, 'удалил:\n', subject, date, group)
	HDB.delete_homework(subject_name=subject, date=date, group=group)
	await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
	await message.answer(
		text=f'*Запись успешно удалена!*', parse_mode='markdown')
	await state.finish()


@dp.callback_query_handler(lambda query: query.data.split('_')[2][0] == 'B', state=SelfState.Delete_state)
async def delete_homework_date(query: types.CallbackQuery, state: FSMContext):
	day = query.data.split("_")[2]
	async with state.proxy() as data:
		date_count = data['date_count']
		start_date = week_definition(date_count, debug=True)
		data['date'] = (start_date + timedelta(days=days[day])).strftime('%d.%m.%Y')
		date = data["date"]
	start_date, end_date = week_definition(date_count, debug=True), week_definition(date_count)[1]
	start_date = start_date.strftime('%d.%m.%Y')
	homework = HDB.is_available_homework_by_date(date=date, group=get_user_group(query.message), data=True)
	homework = list(map(lambda x: x[0], homework))
	await bot.edit_message_text(
		text='*Выберите предмет*' if homework else '*Тут ничего нет :(\nДавай выберем другой день лучше?*',
		chat_id=query.message.chat.id,
		message_id=query.message.message_id,
		parse_mode='markdown',
		reply_markup=Buttons.create_subjects_keyboard(homework) if homework else None
	)
	await asyncio.sleep(0.5)
	if not homework:
		await bot.send_message(
			chat_id=query.message.chat.id,
			text=f"*На какой день задание?\n📅 {start_date} - {end_date} 📅*",
			reply_markup=Buttons.Inline_Date_ADD,
			parse_mode="markdown"
		)


@dp.message_handler(state=SelfState.Group_state)
async def group_state_command(message: types.Message, state: FSMContext):
	await state.finish()
	await message.answer("Нажми на кнопку, чтобы получить домашнее задание.", reply_markup=Buttons.answer_start)
	chat_id = message.chat.id
	user_group = message.text.upper()
	HDB.add_user(chat_id=chat_id, user_group=user_group, username=message.from_user.username)


@dp.message_handler(lambda message: message.text == 'Управление заданиями', state="*")
async def process_add_command(message: types.Message, state: FSMContext):
	await state.finish()
	async with state.proxy() as data:
		data['date_count'] = 0
	print(message.from_user.username, 'управляет заданиями')
	if message.from_user.username in green_list():
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
	start_date = datetime.now()
	await SelfState.Add_state.set()
	await bot.edit_message_text(
		chat_id=call.message.chat.id,
		message_id=call.message.message_id,
		text=f"*Выберите предмет*",
		parse_mode="markdown",
		reply_markup=Buttons.create_subjects_keyboard(get_group_schedule(get_user_group(call.message), start=start_date))
	)


@dp.message_handler(state=SelfState.Parse_state, content_types=types.ContentType.DOCUMENT)
async def parse_attachments(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		date = data['date']
	HDB.attach_file(date=date, filename=message.document.file_id, group=get_user_group(message))


@dp.message_handler(
	state=SelfState.Add_state,
	content_types=[types.ContentType.TEXT, types.ContentType.DOCUMENT, types.ContentType.PHOTO]
)
async def add_homework(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			date = data['date']
			subject = data['subject']
			data['state'] = False
	except KeyError:
		await message.answer(text='Ну ладно 🥺', parse_mode='markdown')
		await state.finish()
		return Ellipsis

	if HDB.is_exists(subject_name=subject, date=date, group=get_user_group(message)):
		await message.reply(text='*Мы уже записывали задание на этот день и на это предмет :)*', parse_mode='markdown')
		await state.finish()
		return Ellipsis

	text = message.text
	print(message.from_user.username, 'добавил:\n', text if text is not None else message.caption)
	user_group = get_user_group(message)
	exercise = text
	if message.document is not None and message.document.file_id is not None:
		await SelfState.Parse_state.set()
		HDB.attach_file(date=date, filename=message.document.file_id, group=user_group)
		exercise = message.caption if message.caption is not None else exercise
	elif message.photo and message.photo[0] is not None:
		await SelfState.Parse_state.set()
		HDB.attach_file(date=date, filename=message.photo[0].file_id, group=user_group)
		exercise = message.caption if message.caption is not None else exercise
	else:
		await state.finish()
	if exercise is not None:
		await message.answer(
			text='*{}*'.format(
				HDB.add_homework(
					subject_name=subject,
					date=date,
					text=exercise,
					username=message.from_user.username,
					group=user_group)), parse_mode='markdown')
	try:
		await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
	except aiogram.utils.exceptions.MessageToDeleteNotFound:
		print('Какое-то сообщение не удаляется(')


@dp.callback_query_handler(text='Inline_Edit')
async def edit_init(call: types.CallbackQuery, state: FSMContext):
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
	text = message.text
	async with state.proxy() as data:
		date = data['date']
		subject = data['subject']
	print(message.from_user.username, 'отредактировал:\n', text)
	HDB.delete_homework(subject_name=subject, date=date, group=get_user_group(message))
	text = HDB.add_homework(
		subject_name=subject,
		username=message.from_user.username,
		text=text, date=date,
		group=get_user_group(message),
		edit=True)
	await message.answer(
		text=f'*{text}*', parse_mode='markdown')
	await state.finish()


@dp.callback_query_handler(lambda query: query.data.split('_')[2][0] == 'B', state=SelfState.Add_state)
async def add_homework_date(query: types.CallbackQuery, state: FSMContext):
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


def register_cq_handlers(dsp: Dispatcher):
	dsp.register_callback_query_handler(callback=callback_up, text='Inline_Date_Up', state='*')
	dsp.register_callback_query_handler(callback=callback_down, text='Inline_Date_Up', state='*')
	dsp.register_callback_query_handler(callback=all_week_homework, text='Inline_Date_Week', state='*')
	dsp.register_callback_query_handler(homework_reply, lambda query: query.data.split('_')[2][0] == 'B')
	dsp.register_callback_query_handler(
		edit_homework_date,
		lambda query: query.data.split('_')[2][0] == 'B',
		state=SelfState.Edit_state)


if __name__ == '__main__':
	register_cq_handlers(dp)
	executor.start_polling(dp, skip_updates=True)
