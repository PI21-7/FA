from config import ADMIN


class Debugger:
    """The current conditions for launching the bot transfer logs to nohup.out"""
    debug = True
    bot = None

    @classmethod
    async def info(cls, user, action, data=None) -> str or None:
        """Вывод в консоль информации о действиях пользователя"""
        if not cls.debug:
            return ...
        if data is None:
            data = ''
        else:
            data = f'\n--> {data}'
        out = f'{user} {action}{data}'
        if cls.bot is None:
            print(out)
        else:
            await cls.bot.send_message(
                chat_id=ADMIN,
                text='`⚡ LOGS:`\n' + f'*{out}*',
                parse_mode='markdown'
            )

    @classmethod
    async def error(cls, data) -> str or None:
        if not cls.debug:
            return ...
        if cls.bot is None:
            print(data)
        else:
            await cls.bot.send_message(
                chat_id=ADMIN,
                text='`⚡⚡ ERROR:`\n' + f'*{data}*',
                parse_mode='markdown'
            )


'''
    С удовольствием пишу для вас обновы!   
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠄⣠⣶⣾⣿⣿⣿⣿⣿⣿⣷⣶⣄⡀⠄⠄⠄⠄⠄
    ⣿⣿⣿⣿⣿⣿⣿⣿⠃⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⠄⠄⠄⠄
    ⣿⣿⣿⣿⣿⣿⣿⠏⣠⡾⠛⠛⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠄⠄
    ⣿⣿⣿⣿⣿⣿⠏⣼⣿⣶⣿⣿⣦⣤⣀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀
    ⣿⣿⣿⣿⣿⡏⣼⣿⡿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠉⠛⠻⣿⣿⣿⣿⣿⡷
    ⣿⣿⣿⣿⡏⣾⣿⣿⣿⣷⣶⣤⣤⣽⣿⣿⣿⣿⣿⣿⣿⣇⠄⠄⠈⢿⣿⣿⣿⡇
    ⣿⣿⣿⢣⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣻⣿⣿⣿⣷⣦⡀⠛⣿⣿⠃
    ⣿⣿⢋⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣍⠻⢿⣿⣿⣷⠄⣸⣿⠄
    ⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣇⣤⣿⡟⠻⣿⣿⣿⣿⣿⣿⣷⣤⣽⣿⣿⣿⣿⣿⠄
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢶⡿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠄
    ⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⣿⣿⣿⣿⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠄⠄
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣬⣍⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠁⠄⠄
    ⡏⡿⣿⣿⣿⣿⣿⣿⣏⣁⡹⠿⣿⣤⣙⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠄⠄⠄⠘
    ⡇⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡇⠄⠄⠄⠄⢀
    ⣿⠄⠄⠉⠉⠻⣿⣿⣿⣿⡝⠻⣿⢛⡛⠻⣿⣿⣿⣿⣿⣿⡿⣆⠑⢎⠄⢀⡃⣼
'''


