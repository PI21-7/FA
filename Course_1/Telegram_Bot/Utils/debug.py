class Debugger:
    """The current conditions for launching the bot transfer logs to nohup.out"""
    debug = True

    @classmethod
    def info(cls, user, action, data=None) -> str or None:
        """Вывод в консоль информации о действиях пользователя"""
        if not cls.debug:
            return ...
        if data is None:
            data = ''
        else:
            data = f'\n--> {data}'
        out = f'{user} {action}{data}'
        print(out)

    @classmethod
    def error(cls, data) -> str or None:
        if not cls.debug:
            return ...
        print(data)

