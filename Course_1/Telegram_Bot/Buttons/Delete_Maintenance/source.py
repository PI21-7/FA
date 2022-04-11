from Course_1.Telegram_Bot.Buttons.__modules__ import *


async def delete_homework_date(query: types.CallbackQuery, state: FSMContext):
	day = query.data.split("_")[2]
	async with state.proxy() as data:
		date_count = data['date_count']
		start_date = week_definition(date_count, debug=True)
		data['date'] = (start_date + timedelta(days=days[day])).strftime('%d.%m.%Y')
		date = data["date"]
	start_date, end_date = week_definition(date_count, debug=True), week_definition(date_count)[1]
	start_date = start_date.strftime('%d.%m.%Y')
	homework = HDB.is_available_homework_by_date(date=date, group=get_user_group(query.message), data=True)
	homework = list(map(lambda x: x[0], homework))
	await bot.edit_message_text(
		text='*Выберите предмет*' if homework else '*Тут ничего нет :(\nДавай выберем другой день лучше?*',
		chat_id=query.message.chat.id,
		message_id=query.message.message_id,
		parse_mode='markdown',
		reply_markup=create_subjects_keyboard(homework) if homework else None
	)
	await asyncio.sleep(0.5)
	if not homework:
		await bot.send_message(
			chat_id=query.message.chat.id,
			text=f"*На какой день задание?\n📅 {start_date} - {end_date} 📅*",
			reply_markup=Inline_Date_ADD,
			parse_mode="markdown"
		)


async def delete_homework(query: types.CallbackQuery, state: FSMContext):
	message = query.message
	async with state.proxy() as data:
		date = data['date']
		date_count = data['date_count']
	schedule = get_group_schedule(group=get_user_group(query.message), start=week_definition(date_count, debug=True))
	transliterated_schedule = list(map(
		lambda x: translit(x, language_code='ru', reversed=True), schedule))
	subject = None
	for pos, let in enumerate(transliterated_schedule):
		if query.data in let:
			subject = schedule[pos]
			break
	group = get_user_group(message)
	debugger.info(message.from_user.username, 'удалил', ' '.join([subject, date, group]))
	HDB.delete_homework(subject_name=subject, date=date, group=group)
	await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
	await message.answer(
		text=f'*Запись успешно удалена!*', parse_mode='markdown')
	await state.finish()


async def delete_homework_state(query: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		data['state'] = True
		date_count = data['date_count']
	start_date, end_date = week_definition(date_count)
	await bot.edit_message_text(
		chat_id=query.message.chat.id,
		message_id=query.message.message_id,
		text=f"*На какой день задание?\n📅 {start_date} - {end_date} 📅*",
		reply_markup=Inline_Date_ADD,
		parse_mode="markdown"
	)
	await SelfState.Delete_state.set()
