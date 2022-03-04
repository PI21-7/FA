# -*- coding: utf-8 -*-
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove

from config import TOKEN
import Buttons


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'], state = "*")
async def process_start_command(message: types.Message):
	await message.answer("Привет! Нажми на кнопку чтобы получить домашнее задание.", reply_markup =  Buttons.answer_start)

@dp.message_handler(lambda message: message.text == 'Получить задание!')
async def process_date(message: types.Message):
	await message.answer("Выбераем дату", reply_markup = Buttons.answer_date)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)