import unittest
import os
from Course_1.Telegram_Bot.db import *


class DatabaseTests(unittest.TestCase):
    Test_DB = Database()

    def test_init(self):
        """
        Тестирование процесса создания базы данных
        """
        Database_NAME = 'TEST_DATABASE'
        Connections.database = f'{Database_NAME}.db'
        self.Test_DB.init(name=Database_NAME)
        self.assertTrue(os.path.exists(Connections.database), 'База данных не создалась или создалась некорректно')


if __name__ == '__main__':
    unittest.main()
