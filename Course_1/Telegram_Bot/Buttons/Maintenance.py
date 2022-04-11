from Course_1.Telegram_Bot.Buttons.Add_Maintenance.source import *
from Course_1.Telegram_Bot.Buttons.Delete_Maintenance.source import *
from Course_1.Telegram_Bot.Buttons.Edit_Maintenance.source import *
from Course_1.Telegram_Bot.Buttons.Reply_Maintenance.source import *


async def callback_down(call: types.CallbackQuery, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['date_count'] += 1
			date_count = data['date_count']
			button_state = data["state"]
			await bot.edit_message_text(
				chat_id=call.message.chat.id,
				message_id=call.message.message_id,
				text=f"*{'Выбираем день недели' if not button_state else 'На какой день задание?'}\n📅 {week_definition(date_count)[0]} - {week_definition(date_count)[1]} 📅*",
				parse_mode="markdown",
				reply_markup=Inline_Date_ADD if button_state else Inline_Date)

	except KeyError:
		pass


async def callback_up(call: types.CallbackQuery, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['date_count'] -= 1
			date_count = data['date_count']
			button_state = data["state"]
		await bot.edit_message_text(
			chat_id=call.message.chat.id,
			message_id=call.message.message_id,
			text=f"*{'Выбираем день недели' if not button_state else 'На какой день задание?'}\n📅 {week_definition(date_count)[0]} - {week_definition(date_count)[1]} 📅*",
			parse_mode="markdown",
			reply_markup=Inline_Date_ADD if button_state else Inline_Date)
	except KeyError:
		pass


async def process_rule_command(message: types.Message, state: FSMContext):
	await state.finish()
	async with state.proxy() as data:
		data['date_count'] = 0
	debugger.info(message.from_user.username, 'управляет заданиями')
	if message.from_user.username in green_list():
		await message.answer(
			text='*Что будем делать?*',
			parse_mode='markdown',
			reply_markup=Inline_Manage
		)

	else:
		await message.answer(
			text='*Вы не можете управлять заданиями, для получения возможности → @Nps_rf или @monotank*',
			parse_mode='markdown')


async def group_state_command(message: types.Message, state: FSMContext):
	await state.finish()
	await message.answer("Нажми на кнопку, чтобы получить домашнее задание.", reply_markup=answer_start)
	chat_id = message.chat.id
	user_group = message.text.upper()
	HDB.add_user(chat_id=chat_id, user_group=user_group, username=message.from_user.username)

