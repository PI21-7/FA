# noinspection INSPECTION_NAME
import aiogram.utils.exceptions
from Buttons.__modules__ import *


async def all_week_homework(call: types.CallbackQuery, state: FSMContext):
	try:
		async with state.proxy() as data:
			date_count = data['date_count']
		start_date = week_definition(date_count, debug=True)
		for day in range(6):
			current_day = (start_date + timedelta(days=day)).strftime('%d.%m.%Y')
			available_homework = HDB.is_available_homework_by_date(
				date=current_day,
				group=get_user_group(call.message),
				data=True)
			__text = ''

			for num, subject in enumerate(available_homework):
				__text += \
					f'{str(num + 1)}) ' + subject[0] + ': ' + subject[1] + '\n'
			if not __text:
				__text = '*Никто не заполнил домашнее задания на этот день* 😭'
			else:
				__text = '`' + __text + '`'
			message = f'*📅 {days_of_week[day + 1]} {current_day}*\n{__text}'
			await call.message.answer(
				text=message,
				parse_mode='markdown')
			if HDB.is_file_attached(group=get_user_group(call.message), date=current_day):
				attachments = HDB.get_attachments(group=get_user_group(call.message), date=current_day)
				for pos, document in enumerate(attachments):
					await bot.send_document(
						chat_id=call.message.chat.id,
						document=document[0],
						caption=None,
						parse_mode='markdown')
		try:
			await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		except MessageToDeleteNotFound:
			Debugger.error('Какое-то сообщение не удаляется(')
	except KeyError:
		await process_start_command(call.message)


async def homework_reply(query: types.CallbackQuery, state: FSMContext):
	day = query.data.split("_")[2]
	try:
		async with state.proxy() as data:
			date_count = data['date_count']
		start_date = week_definition(date_count, debug=True)
		date_to_db = [
			(start_date + timedelta(days=days[day])).strftime('%d.%m.%y'),
			(start_date + timedelta(days=days[day])).strftime('%d.%m.%Y')]

		if HDB.is_available_homework_by_date(
				date=date_to_db[0],
				group=get_user_group(query.message)) or HDB.is_available_homework_by_date(
			date=date_to_db[1],
			group=get_user_group(query.message)):

			date_to_db = date_to_db[0] if HDB.is_available_homework_by_date(
				date=date_to_db[0],
				group=get_user_group(query.message)) else date_to_db[1]

			available_homework = HDB.is_available_homework_by_date(
				date=date_to_db,
				data=True,
				group=get_user_group(query.message))
			__text = str()
			for num, subject in enumerate(available_homework):
				__text += f'{str(num + 1)}) ' + subject[0] + ': ' + subject[1] + '\n'
			text = f'*📅 {days_of_week[days[day] + 1]} {date_to_db}*\n`{__text}`'
			await query.message.answer(
				text=text,
				parse_mode='markdown'
			)
			if HDB.is_file_attached(date=date_to_db, group=get_user_group(query.message)):
				attachments = HDB.get_attachments(group=get_user_group(query.message), date=date_to_db)
				for pos, document in enumerate(attachments):
					await bot.send_document(
						chat_id=query.message.chat.id,
						document=document[0],
						caption=None,
						parse_mode='markdown')
			try:
				await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
			except MessageToDeleteNotFound:
				Debugger.error('Какое-то сообщение не удаляется(')
		else:
			await query.message.answer(
				text='*Никто не заполнил домашнее задания на этот день* 😭', parse_mode='markdown'
			)

	except KeyError:
		await process_start_command(query.message)


async def processing_of_receiving_hw(message: types.Message, state: FSMContext):
	Debugger.info(message.from_user.username, 'получает задание')
	await state.finish()
	async with state.proxy() as data:
		data['date_count'] = 0
		data["state"] = False
	await message.answer(
		f"*Выбираем день недели\n📅 {week_definition(0)[0]} - {week_definition(0)[1]} 📅*",
		parse_mode="markdown", reply_markup=Inline_Date)


async def process_get_materials(message: types.Message, state: FSMContext):
	await state.finish()
	try:
		attachments = HDB.get_attachments_materials(group=get_user_group(message))
		if not attachments:
			await message.answer(
				text='*У нас не нашлось полезных материалов вашей группы.\nМожет их ещё не добавили?*',
				parse_mode='markdown')
		for pos, document in enumerate(attachments):
			await bot.send_document(
				chat_id=message.chat.id,
				document=document[0],
				caption=None,
				parse_mode='markdown')
	except aiogram.utils.exceptions.WrongFileIdentifier:
		await message.answer(
			text='*У нас не нашлось полезных материалов вашей группы.\nМожет их ещё не добавили?*',
			parse_mode='markdown')
		