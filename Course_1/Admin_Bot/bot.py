from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import *
from admin_buttons import Start_buttons
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Course_1.Telegram_Bot.Utils.Maintenance import green_list

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


class SelfState(StatesGroup):
    add_person = State()
    delete_person = State()


@dp.message_handler(commands=['start'], state="*")
async def process_start_command(message: types.Message, state: FSMContext):
    if message.from_user.username not in Admin:
        return await message.answer('*У вас нет доступа к управлению ботом!*', parse_mode='markdown')

    await state.finish()
    await message.answer("Привет нажми на кнопку!", reply_markup=Start_buttons)


@dp.message_handler(lambda message: message.text == 'Добавить',  state="*")
async def add_person(message: types.Message):
    await SelfState.add_person.set()
    await message.answer("Напиши username пользователя!")


@dp.message_handler(lambda message: message.text == 'Удалить',  state="*")
async def add_person(message: types.Message):
    await SelfState.delete_person.set()
    await message.answer("Напиши username пользователя!")


@dp.message_handler(state=SelfState.add_person)
async def add_person_to_file(message: types.Message, state: FSMContext):
    await state.finish()
    with open('../Telegram_Bot/Admin/admins.txt', 'a', encoding='utf-8') as f:
        f.writelines(',' + message.text)
    await message.answer(text='*Пользователь добавлен!*', parse_mode='markdown')


@dp.message_handler(state=SelfState.delete_person)
async def delete_person_from_file(message: types.Message, state: FSMContext):
    await state.finish()
    GL = green_list('../Telegram_Bot/Admin/admins.txt')

    with open('../Telegram_Bot/Admin/admins.txt', 'w') as f:
        f.write(','.join(filter(lambda x: x != message.text, GL)))

    await message.answer(text='*Пользователь удален!*', parse_mode='markdown')


if __name__ == '__main__':
    executor.start_polling(dp)
