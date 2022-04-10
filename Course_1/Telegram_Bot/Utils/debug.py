class Debugger:
    def __init__(self, action: bool = True):
        """
        :type action: bool
        :type_description action: If true, print info, else return info in string form
        """
        assert isinstance(action, bool)
        self.action = action

    def info(self, user, action, data=None) -> str or None:
        """Вывод в консоль информации о действиях пользователя"""
        if data is None:
            data = ''
        else:
            data = f'\n--> {data}'
        out = f'{user} {action}{data}'
        if self.action:
            print(out)
        else:
            return out
