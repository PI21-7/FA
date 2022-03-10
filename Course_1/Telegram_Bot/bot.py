from datetime import timedelta

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
import Buttons
from db import Database
from date import week_definition
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class SelfState(StatesGroup):
	Add_state = State()


storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
db = Database()
db.init()


@dp.message_handler(commands=['start'], state="*")
async def process_start_command(message: types.Message):
	await message.answer("Привет! Нажми на кнопку чтобы получить домашнее задание.", reply_markup=Buttons.answer_start)


@dp.message_handler(lambda message: message.text == 'Добавить задание', state="*")
async def process_add_command(message: types.Message):
	await message.answer(
		text='Вводите домашнее задание в формате:\n*Название предмета  Дата  Задание*',
		parse_mode='markdown'
	)
	await SelfState.Add_state.set()


@dp.message_handler(state=SelfState.Add_state)
async def add_homework(message: types.Message, state: FSMContext):
	await state.finish()
	text = message.text.split()
	Subject, Date, Exercise = text[0], text[1], ' '.join(text[2:])
	db.add_homework(subject_name=Subject, date=Date, text=Exercise)


@dp.callback_query_handler(lambda query: query.data.split('_')[2][0] == 'B')
async def homework_reply(query: types.CallbackQuery, state: FSMContext):
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
		date_to_db = start_date + timedelta(days=days[query.data.split('_')[2]])
		print(date_to_db)
		print(query.data.split('_'))
	except KeyError as e:
		print(True, e)
		await process_start_command(query.message)


@dp.message_handler(lambda message: message.text == 'Получить задание!',  state="*")
async def process_date(message: types.Message, state: FSMContext):
	await state.finish()
	async with state.proxy() as data:
		data['date_count'] = 0
	await message.answer(
		f"*Выбираем дату \n{week_definition(0)[0]} - {week_definition(0)[1]}*",
		parse_mode="markdown", reply_markup=Buttons.Inline_Date)


@dp.callback_query_handler(text="Inline_Date_Down")
async def callback_down(call: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		data['date_count'] += 1
		date_count = data['date_count']
	await bot.edit_message_text(
		chat_id=call.message.chat.id,
		message_id=call.message.message_id,
		text=f"*Выбираем дату \n{week_definition(date_count)[0]} - {week_definition(date_count)[1]}*",
		parse_mode="markdown",
		reply_markup=Buttons.Inline_Date)


@dp.callback_query_handler(text="Inline_Date_Up")
async def callback_up(call: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		data['date_count'] -= 1
		date_count = data['date_count']
	await bot.edit_message_text(
		chat_id=call.message.chat.id,
		message_id=call.message.message_id,
		text=f"*Выбираем дату \n{week_definition(date_count)[0]} - {week_definition(date_count)[1]}*",
		parse_mode="markdown",
		reply_markup=Buttons.Inline_Date)


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
