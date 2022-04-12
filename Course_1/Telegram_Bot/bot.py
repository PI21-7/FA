############################################
from Utils.Miscellaneous import *
from registration import *
############################################
from Utils.debug import Debugger
from aiogram import types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
############################################


@dp.message_handler(commands=['start'], state="*")
async def process_start_command(message: types.Message):
	await message.answer("Привет! Для получения задания, скажи из какой ты группы!\n\nНапример: ПИ21-7")
	await SelfState.Group_state.set()


@dp.message_handler(state=SelfState.Materials_parse_state, content_types=types.ContentType.DOCUMENT)
async def parse_attachments(message: types.Message, state: FSMContext):
	HDB.attach_file_materials(file_id=message.document.file_id, file_name=message.document.file_name, group=get_user_group(message))


@dp.message_handler(content_types=types.ContentType.DOCUMENT, state=SelfState.Materials_state)
async def process_add_material_command(message: types.Message, state: FSMContext):
	await state.finish()
	await SelfState.Materials_parse_state.set()
	if HDB.is_file_attached_materials(group=get_user_group(message), file_name=message.document.file_name):
		HDB.attach_file_materials(
			file_id=message.document.file_id,
			group=get_user_group(message),
			file_name=message.document.file_name)
		await message.answer("материалы добавлены")
	else:
		await message.answer("этот файл уже добавлен!")


@dp.message_handler(state=SelfState.Materials_state)
async def process_answer_by_document(message: types.Message, state: FSMContext):
	await state.finish()
	await message.answer("Надо было отправить просто файл😭")


@dp.callback_query_handler(text='Inline_Materials')
async def materials_state(call: types.CallbackQuery, state: FSMContext):
	await bot.send_message(
			chat_id=call.message.chat.id,
			text="Прикрепите материалы",
			parse_mode="markdown"
		)
	await SelfState.Materials_state.set()


def __sys_arguments(*args, **_kwargs):
	for argument in args[1:]:
		if argument == '-i' or argument == '--init':
			HDB.init()
			continue
		if argument == '-s' or argument == '--silent':
			Debugger.debug = False
			continue
		else:
			exit(f'Unknown argument --> "{argument}"')


if __name__ == '__main__':
	__sys_arguments(*sys.argv)
	overall_handlers_registration(dp)
	executor.start_polling(dp, skip_updates=True)
