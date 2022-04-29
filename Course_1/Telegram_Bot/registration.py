from aiogram import Dispatcher as _Dispatcher
from Buttons.Maintenance import *


def register_cq_handlers(dp: _Dispatcher):
	dp.register_callback_query_handler(callback=callback_up, text='Inline_Date_Up', state='*')
	dp.register_callback_query_handler(callback=callback_down, text='Inline_Date_Down', state='*')
	dp.register_callback_query_handler(callback=all_week_homework, text='Inline_Date_Week', state='*')
	dp.register_callback_query_handler(
		homework_reply,
		lambda query: query.data.split('_')[2][0] == 'B' if len(query.data.split('_')) > 2 else False)
	dp.register_callback_query_handler(
		editor_homework_date,
		lambda query: query.data.split('_')[2][0] == 'B' if len(query.data.split('_')) > 2 else False,
		state=SelfState.Edit_state)
	dp.register_callback_query_handler(
		add_homework_date,
		lambda query: query.data.split('_')[2][0] == 'B' if len(query.data.split('_')) > 2 else False,
		state=SelfState.Add_state
	)
	dp.register_callback_query_handler(manual_input_state, text='Inline_Manual_Input', state='*')
	dp.register_callback_query_handler(edit_init, text='Inline_Edit')
	dp.register_callback_query_handler(add_homework_state, text='Inline_Add')
	dp.register_callback_query_handler(
		delete_homework_date,
		lambda query: query.data.split('_')[2][0] == 'B' if len(query.data.split('_')) > 2 else False,
		state=SelfState.Delete_state)
	dp.register_callback_query_handler(
		delete_homework,
		lambda query: 'Inline' not in query.data,
		state=SelfState.Delete_state)
	dp.register_callback_query_handler(delete_homework_state, text='Inline_Delete')
	dp.register_callback_query_handler(
		editor_add_homework_subject,
		lambda query: 'Inline' not in query.data,
		state=SelfState.Edit_state)
	dp.register_callback_query_handler(
		adding_add_homework_subject,
		lambda query: 'Inline' not in query.data,
		state=SelfState.Add_state)
	dp.register_callback_query_handler(
		faculty_state_command,
		state=SelfState.Faculty_state
	)
	dp.register_callback_query_handler(
		group_state_command,
		state=SelfState.Group_state
	)
	dp.register_callback_query_handler(
		groups_state_command,
		state=SelfState.Groups_state
	)
	dp.register_callback_query_handler(answer_about_questions, text='Inline_Question_Why', state='*')
	dp.register_callback_query_handler(delete_materials_state, text='Inline_Manage_Materials', state='*')
	dp.register_callback_query_handler(delete_materials, state=SelfState.Delete_materials_state)


def register_msg_handlers(dp: _Dispatcher):
	dp.register_message_handler(
		processing_of_receiving_hw,
		lambda message: message.text == 'Получить задание',
		state="*")
	dp.register_message_handler(
		process_rule_command,
		lambda message: message.text == 'Управление заданиями',
		state="*")
	dp.register_message_handler(
		process_get_materials,
		lambda message: message.text == 'Полезные материалы группы',
		state="*")
	dp.register_message_handler(edit_homework, state=SelfState.Edit_state)
	dp.register_message_handler(
		add_homework,
		state=SelfState.Add_state,
		content_types=[types.ContentType.TEXT, types.ContentType.DOCUMENT, types.ContentType.PHOTO])
	dp.register_message_handler(
		parse_attachments,
		state=SelfState.Parse_state,
		content_types=types.ContentType.DOCUMENT)

	dp.register_message_handler(process_start_command, commands=['start'], state="*")
	dp.register_message_handler(process_about_command, commands=['about'], state="*")
	dp.register_message_handler(process_warnings_command, commands=['warnings'], state='*')
	dp.register_message_handler(manual_input, state=SelfState.Manual_input_state)


def overall_handlers_registration(dp: _Dispatcher):
	register_cq_handlers(dp)
	register_msg_handlers(dp)
