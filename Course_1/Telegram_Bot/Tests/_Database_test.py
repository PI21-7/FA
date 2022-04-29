import unittest
import os
from Course_1.Telegram_Bot.Database import *


class DatabaseTests(unittest.TestCase):
    Test_DB = Database()

    def test_creation(self):
        Database_NAME = 'TEST_DATABASE'
        Connections.database = f'{Database_NAME}.db'
        self.Test_DB.init()
        self.assertTrue(os.path.exists(Connections.database), 'База данных не создалась или создалась некорректно')
        if os.path.exists(Connections.database):
            os.remove(Connections.database)


if __name__ == '__main__':
    unittest.main()
