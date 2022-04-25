import asyncio

from Buttons.__modules__ import *


async def process_start_command(message: types.Message):
    await message.answer(
        text="*Привет!\nДавай сначала найдем твой факультет?*",
        parse_mode='markdown', reply_markup=create_faculties_keyboard(Groups.get_faculties_list()))
    global __user
    __user = message.from_user.username
    await SelfState.Faculty_state.set()


async def manual_input_state(query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    message = query.message
    await bot.delete_message(message.chat.id, message_id=message.message_id)
    await message.answer(f"Хорошо, введи свою группу!\n\n*Например: ПИ21-7*",
                         reply_markup=answer_start, parse_mode='markdown')
    await SelfState.Manual_input_state.set()


async def manual_input(message: types.Message, state: FSMContext):
    await state.finish()
    chat_id = message.chat.id
    user_group = message.text
    await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
    await Debugger.info(message.from_user.username, 'зарегистрировался', f'\nгруппа {user_group}')
    await message.answer(f"Отлично!\nМы записали что ты из группы *{user_group}*.\n"
                         f"Нажми на кнопку, чтобы получить домашнее задание!\n"
                         f"Команды:\n/start - *Вернуться к выбору группы*\n/about - *Информация о нас*\n/warnings - "
                         f"*Свод правил*",
                         reply_markup=answer_start, parse_mode='markdown')
    HDB.add_user(chat_id=chat_id, user_group=user_group, username=message.from_user.username)


async def faculty_state_command(query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    faculties = Groups.get_faculties_list()
    faculty = translit(query.data, language_code='ru')
    for item in faculties:
        if faculty.lower() in item.lower():
            faculty = item
            break
        if faculty.lower().strip() == 'економических отношений':  # Bug
            faculty = 'Факультет международных экономических отношений'
            break
    await bot.edit_message_text(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        text='*Давай теперь выберем направление?*',
        reply_markup=create_faculties_keyboard(Groups.get_groups_types(Groups.get_groups_by_faculty(faculty))),
        parse_mode='markdown')
    await SelfState.Groups_state.set()


async def groups_state_command(query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    initial = translit(query.data, language_code='ru').upper()
    await bot.edit_message_text(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        text='*А теперь группу!*',
        reply_markup=create_faculties_keyboard(Groups.get_groups_by_initial(initial)),
        parse_mode='markdown')
    await SelfState.Group_state.set()


async def group_state_command(query: types.CallbackQuery, state: FSMContext):
    message = query.message
    chat_id = message.chat.id
    user_group = translit(query.data, language_code='ru').upper()
    await bot.delete_message(message.chat.id, message_id=message.message_id)
    await message.answer(f"Отлично!\nМы записали что ты из группы *{user_group}*.\n"
                         f"Нажми на кнопку, чтобы получить домашнее задание!\n"
                         f"Команды:\n/start - *Вернуться к выбору группы*\n/about - *Информация о нас*\n/warnings - "
                         f"*Свод правил*",
                         reply_markup=answer_start, parse_mode='markdown')
    await Debugger.info(__user, 'зарегистрировался', f'группа {user_group}')
    HDB.add_user(chat_id=chat_id, user_group=user_group, username=__user)
    await state.finish()


async def process_about_command(message: types.Message):
    await message.answer('*Домашние задания Финансового Университета* — неофициальный бот созданный группой '
                         'энтузиастов с кафедры [ИТиАБД](https://vk.com/itbda2000) Финансового Университета при '
                         'Правительстве Российской Федерации.'
                         '\n\n`Данный бот призван облегчить '
                         'поиск/получение домашних заданий для студентов.`', parse_mode='markdown',
                         reply_markup=Inline_About_Questions)


async def process_warnings_command(message: types.Message):
    await message.answer('*Для предупреждения каких-либо проблем, у нас, а потом и у вас, давайте все будем '
                         'придерживаться общих правил:*\n'
                         '`1) Просьба не удалять и не изменять задания других групп для "веселья", "забавы" и прочего\n'
                         '\t1.1) То же самое касается и своей группы\n'
                         '2) Просьба соблюдать этические нормы и не записывать ДЗ с использование любых бранных слов '
                         'и выражений, употребление которых не допускается общественной моралью\n'
                         '3) Если сложилось ощущение что какие-то выходки останутся безнаказанными, то увы, '
                         'спешу вас разочаровать, все логи приходят ко мне в админ панель 😔\n'
                         '4) Если уж сложилась такая ситуация, что какой-то пункт был нарушен, сожалею, '
                         'но в течение часа, доступ к каким-либо взаимодействиям с ДЗ, вы потеряете :(`\n'
                         '_С уважением,_ [представитель команды разработки](https://vk.com/itbda2000).',

                         parse_mode='markdown')


async def answer_about_questions(query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await query.message.answer('*Рассмотрим следующую ситуацию:*\n'
                               'Четверг: прошла пара по вышмату, задали дз до следующего четверга...\n',
                               parse_mode='markdown')
    await asyncio.sleep(2.5)
    await query.message.answer('*Наступает суббота*\n', parse_mode='markdown')
    await asyncio.sleep(2.5)
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
