"""
------------------------------------------------------
| DOCUMENTATION LANGUAGE || RU & ENG   			     |
| Created by Nps-rf 	 || 03.03.2022		   	     |
| Edited by Nps-rf	     || 26.04.2022			     |
| Email				     || Divine.Nikolai@Gmail.com |
------------------------------------------------------
"""
############################################
from Utils.Miscellaneous import *
from registration import *
############################################
from Utils.debug import Debugger
from aiogram import types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
############################################


@dp.message_handler(state=SelfState.Materials_parse_state, content_types=types.ContentType.DOCUMENT)
async def parse_attachments(message: types.Message):
	HDB.attach_file_materials(
		file_id=message.document.file_id,
		file_name=message.document.file_name,
		group=get_user_group(message))


@dp.message_handler(content_types=types.ContentType.DOCUMENT, state=SelfState.Materials_state)
async def process_add_material_command(message: types.Message, state: FSMContext):
	await state.finish()
	await SelfState.Materials_parse_state.set()
	if HDB.is_file_attached_materials(group=get_user_group(message), file_name=message.document.file_name):
		HDB.attach_file_materials(
			file_id=message.document.file_id,
			group=get_user_group(message),
			file_name=message.document.file_name)
		await message.answer("*Материалы добавлены*", parse_mode='markdown')
	else:
		await message.answer("*Этот файл уже добавлен!*", parse_mode='markdown')


@dp.message_handler(state=SelfState.Materials_state)
async def process_answer_by_document(message: types.Message, state: FSMContext):
	await state.finish()
	await message.answer("*Надо было отправить просто файл*😭", parse_mode='markdown')


@dp.callback_query_handler(text='Inline_Materials')
async def materials_state(query: types.CallbackQuery, state: FSMContext):
	await state.finish()
	await bot.edit_message_text(
		chat_id=query.message.chat.id,
		message_id=query.message.message_id,
		text="*Прикрепите материалы*\n\n*Постарайтесь давать файлам название,* "
			 "`отчетливо` *дающее понять содержание и назначение файла*",
		parse_mode="markdown"
	)
	await SelfState.Materials_state.set()


async def __send_info_for_users__(important: bool = False):
	UID_s = list(map(lambda x: x[0], HDB.all_users()))
	for UID in UID_s:
		try:
			await bot.send_message(
				chat_id=None,
				text=None,
				parse_mode='markdown',
				disable_notification=not important)
		except Exception as e:
			sys.stdout.write(f'{e} {UID}')


async def __sys_arguments(*_) -> None:
	"""
	Synology run commands:
		1) Telegram_bot -> nohup nice -n -15 python bot.py -t
		2) Admin_bot -> nohup nice -n 0 python bot.py
	Synology SD commands:
		1) sudo killall python
	commands:
		nohup: to pass shutting down due to breaking SSH tunnel.
		nice: to run file with priority you need.
		killall: ? idk
	:return: None
	"""
	for argument in sys.argv[1:]:
		if argument in ('-i', '--init'):
			HDB.init()  # Инициализация базы данных (Только при первом запуске бота)
			continue
		elif argument in ('-s', '--silent'):
			Debugger.debug = False  # Вывод в консоль | (Логов в Nohup.out не будет)
			continue
		elif argument in ('-t', '--telegram'):
			Debugger.bot = admin_bot
		elif argument in ('-n', '--notice'):
			await __send_info_for_users__()
			continue
		else:
			exit(f'Unknown argument --> "{argument}"')


if __name__ == '__main__':
	overall_handlers_registration(dp)
	executor.start_polling(dp, skip_updates=True, on_startup=__sys_arguments)
