############################################
from Utils.Miscellaneous import *
from registration import *
from Utils.Phrases import *
############################################
from Utils.debug import Debugger
from aiogram import types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
############################################


@dp.message_handler(state=SelfState.Materials_parse_state, content_types=types.ContentType.DOCUMENT)
async def parse_attachments(message: types.Message, state: FSMContext):
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
		await message.answer(Mat_added, parse_mode='markdown')
	else:
		await message.answer(Mat_already, parse_mode='markdown')


@dp.message_handler(state=SelfState.Materials_state)
async def process_answer_by_document(message: types.Message, state: FSMContext):
	await state.finish()
	await message.answer(Mat_wrong, parse_mode='markdown')


@dp.callback_query_handler(text='Inline_Materials')
async def materials_state(call: types.CallbackQuery, state: FSMContext):
	await state.finish()
	await bot.send_message(
			chat_id=call.message.chat.id,
			text=Mat_attach,
			parse_mode="markdown"
		)
	await SelfState.Materials_state.set()


def __sys_arguments(*args, **_kwargs):
	for argument in args[1:]:
		if argument == '-i' or argument == '--init':
			HDB.init()  # Инициализация базы данных (Только при первом запуске)
			continue
		if argument == '-s' or argument == '--silent':
			Debugger.debug = False  # Вывод в консоль (Логов в Nohup.out не будет)
			continue
		else:
			exit(f'Unknown argument --> "{argument}"')


if __name__ == '__main__':
	__sys_arguments(*sys.argv)
	overall_handlers_registration(dp)
	executor.start_polling(dp, skip_updates=True)
