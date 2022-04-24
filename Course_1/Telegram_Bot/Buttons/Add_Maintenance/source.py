from ..__modules__ import *


async def add_homework_state(call: types.CallbackQuery):
	start_date = datetime.now()
	await SelfState.Add_state.set()
	await bot.edit_message_text(
		chat_id=call.message.chat.id,
		message_id=call.message.message_id,
		text=f"*Выберите предмет*",
		parse_mode="markdown",
		reply_markup=create_subjects_keyboard(get_group_schedule(get_user_group(call.message), start=start_date))
	)


async def add_homework(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			date = data['date']
			subject = data['subject']
			data['state'] = False
	except KeyError:
		await message.answer(text='Ну ладно 🥺', parse_mode='markdown')
		await state.finish()
		return Ellipsis

	if HDB.is_exists(subject_name=subject, date=date, group=get_user_group(message)):
		await message.reply(text='*Мы уже записывали задание на этот день и на этот предмет :)*', parse_mode='markdown')
		await state.finish()
		return Ellipsis

	text = message.text
	await Debugger.info(message.from_user.username, 'добавил', text if text is not None else message.caption)
	user_group = get_user_group(message)
	exercise = text
	if message.document is not None and message.document.file_id is not None:
		await SelfState.Parse_state.set()
		HDB.attach_file(date=date, filename=message.document.file_id, group=user_group)
		exercise = message.caption if message.caption is not None else exercise
	elif message.photo and message.photo[0] is not None:
		await SelfState.Parse_state.set()
		HDB.attach_file(date=date, filename=message.photo[0].file_id, group=user_group)
		exercise = message.caption if message.caption is not None else exercise
	else:
		await state.finish()
	if exercise is not None:
		await message.answer(
			text='*{}*'.format(
				HDB.add_homework(
					subject_name=subject,
					date=date,
					text=exercise,
					username=message.from_user.username,
					group=user_group)), parse_mode='markdown')
	try:
		await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
	except MessageToDeleteNotFound:
		await Debugger.error('Какое-то сообщение не удаляется(')


async def parse_attachments(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		date = data['date']
	HDB.attach_file(date=date, filename=message.document.file_id, group=get_user_group(message))


async def adding_add_homework_subject(query: types.CallbackQuery, state: FSMContext):
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
		if subject is None:
			async with state.proxy() as data:
				subject = data['subject']

		async with state.proxy() as data:
			data['subject'] = subject
		start_date, end_date = week_definition(date_count)
		await bot.edit_message_text(
			chat_id=query.message.chat.id,
			message_id=query.message.message_id,
			text=f'*На какой день задание?\n📅 {start_date} - {end_date} 📅*',
			reply_markup=Inline_Date_ADD,
			parse_mode='markdown')
	except KeyError as e:
		await Debugger.error(e)


async def add_homework_date(query: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		current_state = data['state']
		date_count = data['date_count']
	if current_state:
		day = query.data.split("_")[2]
		start_date = week_definition(date_count, debug=True)
		await bot.edit_message_text(
			text='*Введите домашнее задание*',
			chat_id=query.message.chat.id,
			message_id=query.message.message_id,
			parse_mode='markdown'
		)
		async with state.proxy() as data:
			data['date'] = (start_date + timedelta(days=days[day])).strftime('%d.%m.%Y')
		await SelfState.Add_state.set()
