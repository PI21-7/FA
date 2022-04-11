############################################
import transliterate as tr				   #
############################################
from Utils.Maintenance import *			   #
from Buttons.Maintenance import *		   #
from Buttons import Buttons				   #
############################################
from aiogram import types				   #
from aiogram.utils import executor		   #
from Utils.date import week_definition	   #
from aiogram.dispatcher import FSMContext  #
############################################

debugger = Debugger()


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
		debugger.error(e)


@dp.message_handler(lambda message: message.text == 'Получить задание!',  state="*")
async def process_date(message: types.Message, state: FSMContext):
	debugger.info(message.from_user.username, 'получает задание')
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
		debugger.error(e)


@dp.callback_query_handler(text='Inline_Delete')
async def delete_homework_state(query: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		data['state'] = True
		date_count = data['date_count']
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
	debugger.info(message.from_user.username, 'удалил', ' '.join([subject, date, group]))
	HDB.delete_homework(subject_name=subject, date=date, group=group)
	await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
	await message.answer(
		text=f'*Запись успешно удалена!*', parse_mode='markdown')
	await state.finish()


def _register_cq_handlers(dsp: Dispatcher):
	dsp.register_callback_query_handler(callback=callback_up, text='Inline_Date_Up', state='*')
	dsp.register_callback_query_handler(callback=callback_down, text='Inline_Date_Up', state='*')
	dsp.register_callback_query_handler(callback=all_week_homework, text='Inline_Date_Week', state='*')
	dsp.register_callback_query_handler(
		homework_reply,
		lambda query: query.data.split('_')[2][0] == 'B' if len(query.data.split('_')) > 2 else False)
	dsp.register_callback_query_handler(
		edit_homework_date,
		lambda query: query.data.split('_')[2][0] == 'B' if len(query.data.split('_')) > 2 else False,
		state=SelfState.Edit_state)
	dsp.register_callback_query_handler(
		add_homework_date,
		lambda query: query.data.split('_')[2][0] == 'B' if len(query.data.split('_')) > 2 else False,
		state=SelfState.Add_state
	)
	dsp.register_callback_query_handler(edit_init, text='Inline_Edit')
	dsp.register_callback_query_handler(add_homework_state, text='Inline_Add')
	dsp.register_callback_query_handler(
		delete_homework_date,
		lambda query: query.data.split('_')[2][0] == 'B' if len(query.data.split('_')) > 2 else False,
		state=SelfState.Delete_state)


def _register_msg_handlers(dsp: Dispatcher):
	dsp.register_message_handler(edit_homework, state=SelfState.Edit_state)
	dsp.register_message_handler(
		add_homework,
		state=SelfState.Add_state,
		content_types=[types.ContentType.TEXT, types.ContentType.DOCUMENT, types.ContentType.PHOTO])
	dsp.register_message_handler(
		parse_attachments,
		state=SelfState.Parse_state,
		content_types=types.ContentType.DOCUMENT)
	dsp.register_message_handler(
		process_add_command,
		lambda message: message.text == 'Управление заданиями',
		state="*")
	dsp.register_message_handler(
		group_state_command,
		state=SelfState.Group_state
	)


def overall_handlers_registration(dsp: Dispatcher):
	_register_cq_handlers(dsp)
	_register_msg_handlers(dsp)


if __name__ == '__main__':
	overall_handlers_registration(dp)
	executor.start_polling(dp, skip_updates=True)
