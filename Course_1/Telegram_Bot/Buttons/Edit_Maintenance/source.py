from Buttons.__modules__ import *


async def editor_homework_date(query: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		current_state = data['state']
		date_count = data['date_count']
	if current_state:
		day = query.data.split("_")[2]

		start_date, end_date = week_definition(date_count, debug=True), week_definition(date_count)[1]
		async with state.proxy() as data:
			data['date'] = (start_date + timedelta(days=days[day])).strftime('%d.%m.%Y')
			date = data["date"]
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


async def edit_homework(message: types.Message, state: FSMContext):
	text = message.text
	async with state.proxy() as data:
		date = data['date']
		subject = data['subject']
	Debugger.info(message.from_user.username, 'отредактировал', text)
	HDB.delete_homework(subject_name=subject, date=date, group=get_user_group(message))
	text = HDB.add_homework(
		subject_name=subject,
		username=message.from_user.username,
		text=text, date=date,
		group=get_user_group(message),
		edit=True)
	await message.answer(
		text=f'*{text}*', parse_mode='markdown')
	await state.finish()


async def edit_init(call: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		data['state'] = True
		date_count = data['date_count']
	start_date, end_date = week_definition(date_count)
	await bot.edit_message_text(
		chat_id=call.message.chat.id,
		message_id=call.message.message_id,
		text=f"*На какой день задание?\n📅 {start_date} - {end_date} 📅*",
		reply_markup=Inline_Date_ADD,
		parse_mode="markdown"
	)
	await SelfState.Edit_state.set()


async def editor_add_homework_subject(query: types.CallbackQuery, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['subject'] = query.conf
			date_count = data['date_count']
			data["state"] = True

		schedule = get_group_schedule(group=get_user_group(query.message), start=week_definition(date_count, debug=True))
		transliterated_schedule = list(map(
			lambda x: translit(x, language_code='ru', reversed=True), schedule))
		subject = None
		for pos, let in enumerate(transliterated_schedule):
			if query.data in let:
				subject = schedule[pos]
				break
		async with state.proxy() as data:
			data['subject'] = subject
		await bot.edit_message_text(
			chat_id=query.message.chat.id,
			message_id=query.message.message_id,
			text=f'*Введите новое задание*',
			parse_mode='markdown')
	except KeyError as e:
		Debugger.error(e)
