import asyncio

from Buttons.__modules__ import *


async def process_start_command(message: types.Message):
    await message.answer(
        text="Привет! Для получения задания, скажи из какой ты группы!\n\nНапример: *ПИ21-7*",
        parse_mode='markdown')
    await SelfState.Group_state.set()


async def process_about_command(message: types.Message):  # If IDE marks it's as error (below), you can **** it away.
    await message.answer('*Домашние задания Финансового Университета* — неофициальный бот созданный группой '
                         'энтузиастов с кафедры [ИТиАБД](https://vk.com/itbda2000) Финансового Университета при '
                         'Правительстве Российской Федерации.'
                         '\n\n`Данный бот призван облегчить '
                         'поиск/получение домашних заданий для студентов.`', parse_mode='markdown',
                         reply_markup=Inline_About_Questions)


async def answer_about_questions(query: types.CallbackQuery):
    await query.message.answer('*Рассмотрим следующую ситуацию:*\n'
                               'Четверг: прошла пара по вышмату, задали дз до следующего четверга...\n',
                               parse_mode='markdown')
    await asyncio.sleep(2.5)
    await query.message.answer('*Наступает Суббота*\n', parse_mode='markdown')
    await asyncio.sleep(2)
    await query.message.answer('🙎‍♂` А что матану задали?`\n', parse_mode='markdown')
    await asyncio.sleep(2)
    await query.message.answer('🙍‍♀` Пункт 10.1. Понятие о дифференциальном уравнении. '
                               'Общее и частное решение уравнения. Задача Коши`', parse_mode='markdown')
    await asyncio.sleep(2)
    await query.message.answer('🙎‍♂` Спасибо!`', parse_mode='markdown')
    await asyncio.sleep(2)
    await query.message.answer('*Наступает понедельник*', parse_mode='markdown')
    await asyncio.sleep(2)
    await query.message.answer('🤷‍♂` А че по матану-то задали?`\n', parse_mode='markdown')
    await asyncio.sleep(2)
    await query.message.answer('🤦‍♀` Выше писали, пролистай`', parse_mode='markdown')
    await asyncio.sleep(2)
    await query.message.answer('🤷‍♂` Те че, сложно ответить?`', parse_mode='markdown')
    await asyncio.sleep(2)
    await query.message.answer('🤦‍♀` А тебе пролистать не судьба?` 🙄\n', parse_mode='markdown')
    await asyncio.sleep(2)
    await query.message.answer('🤷‍♂` Не судьба.`\n', parse_mode='markdown')
    await asyncio.sleep(2)
    await query.message.answer('🤦‍♀` Господи... Пункт 10.1. Понятие о дифференциальном уравнении. '
                               'Общее и частное решение уравнения. Задача Коши`', parse_mode='markdown')
    await asyncio.sleep(2)
    await query.message.answer('🤷‍♂` Спасибо!` 😘', parse_mode='markdown')
    await asyncio.sleep(3)
    await query.message.answer('*Я надеюсь вы поняли, чем же мы мотивировались при создании этого бота* 🤡',
                               parse_mode='markdown')