# -*- coding: utf-8 -*-
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove

from config import TOKEN
import Buttons
import db
import date
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage = storage)
db = db.Database()

@dp.message_handler(commands=['start'], state="*")
async def process_start_command(message: types.Message):
	await message.answer("Привет! Нажми на кнопку чтобы получить домашнее задание.", reply_markup=Buttons.answer_start)


@dp.message_handler(lambda message: message.text == 'Получить задание!',  state = "*")
async def process_date(message: types.Message, state: FSMContext):
	await state.finish()
	async with state.proxy() as data:
		data['date_count'] = 0
	await message.answer(f"*Выбираем дату \n{date.week_definition(0)[0]} {date.week_definition(0)[1]}*", parse_mode="markdown", reply_markup=Buttons.Inline_Date)


@dp.callback_query_handler(text = "Inline_Date_Down")
async def callback(call: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		data['date_count'] += 1
		date_count = data['date_count']


	await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, 
		text = f"*Выбираем дату \n{date.week_definition(date_count)[0]} {date.week_definition(date_count)[1]}*", parse_mode="markdown",  reply_markup=Buttons.Inline_Date)

	async with state.proxy() as data:
		if date.week_definition(date_count)[2] == False:
			data['date_count'] -= 1


@dp.callback_query_handler(text = "Inline_Date_Up")
async def callback(call: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		data['date_count'] -= 1
		date_count = data['date_count']


	await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id,
		text = f"*Выбираем дату \n{date.week_definition(date_count)[0]} {date.week_definition(date_count)[1]}*", parse_mode="markdown",  reply_markup=Buttons.Inline_Date)
	
	async with state.proxy() as data:
		if date.week_definition(date_count)[2] == False:
			data['date_count'] += 1




if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)