import sqlite3

from typing import List, Tuple


class Connections(object):
    database = 'Homework.db'

    @staticmethod
    def safe(func):
        def inside(*args, **kwargs):
            with sqlite3.connect(Connections.database) as connection:
                result = func(*args, connection=(connection, connection.cursor()), **kwargs)
            return result
        return inside


class Database(object):

    class UsersDB(object):
        @Connections.safe
        def init(self, connection: tuple):
            connection, cursor = connection
            cursor.execute('''create table if not exists Users (
            id          INTEGER primary key,
            chat_id     TEXT not null,
            user_group  TEXT not null 
            )''')
            connection.commit()

        @Connections.safe
        def add_user(self, connection: tuple, chat_id: str, user_group: str):
            connection, cursor = connection
            cursor.execute('''INSERT INTO Users (chat_id, user_group) VALUES (?, ?)''', (chat_id, user_group.upper()))

        @Connections.safe
        def get_user_group(self, connection: tuple, chat_id: str) -> str:
            connection, cursor = connection
            cursor = cursor.execute('''SELECT user_group FROM Users WHERE chat_id = ?''', (chat_id,)).fetchall()
            return cursor

    @Connections.safe
    def init(self, connection: tuple, name: str = 'Homework') -> None:
        connection, cursor = connection
        cursor.execute(
            f'create table if not exists {name}('
            f'id         INTEGER primary key,'
            f'subject_id int  not null,'
            f'date       text not null,'
            f'text       TEXT not null)')

        connection.commit()

    @Connections.safe
    def add_homework(self, connection: tuple, subject_name: str, text: str, date: str, username: str) -> str:
        is_added = self.receive_homework(subject_name=subject_name, date=date)
        subject_name = subject_name.lower()
        if is_added:
            return 'Запись уже присутствует'
        connection, cursor = connection
        # Записываем
        cursor.execute('''INSERT INTO Homework (subject_id, date, text, Author) VALUES (?, ?, ?, ?)''',
                       (subject_name, date, text, username))
        connection.commit()
        return 'Домашнее задание добавлено'

    @Connections.safe
    def is_available_homework_by_date(self, connection: tuple, date: str, data=False):
        connection, cursor = connection
        cursor = cursor.execute('''SELECT subject_id, text FROM Homework WHERE date = ?''', (date,)).fetchall()
        connection.commit()
        if data:
            return cursor

        if cursor:
            return True
        return False

    @Connections.safe
    def is_exists(self, connection: tuple, subject_name: str, date: str):
        connection, cursor = connection
        subject_name = subject_name.lower()
        cursor = cursor.execute(
            '''SELECT subject_id and date FROM Homework WHERE subject_id = ? and date = ?''',
            (subject_name, date)).fetchall()
        connection.commit()
        if cursor:
            return True
        return False

    @Connections.safe
    def receive_homework(self, connection: tuple, subject_name: str, date: str) -> str or List[Tuple[str]]:
        subject_name = subject_name.lower()
        connection, cursor = connection
        answer = cursor.execute(
            '''SELECT text FROM Homework WHERE subject_id = ? and date = ? ''',
            (subject_name, date)).fetchall()
        connection.commit()
        if not answer:
            return answer
        return answer[0][0]

    @Connections.safe
    def edit_homework(self, connection: tuple, subject_name: str, date: str, text: str):
        connection, cursor = connection
        subject_name = subject_name.lower()
        cursor.execute(
            '''UPDATE Homework SET text = ? WHERE subject_id = ? and date = ?;''', (text, subject_name, date)
        )
        connection.commit()

    @Connections.safe
    def delete_homework(self, connection: tuple, subject_name: str, date: str) -> None:
        connection, cursor = connection
        subject_name = subject_name.lower()
        cursor.execute('''
        DELETE FROM Homework WHERE subject_id = ? and date = ?;''', (subject_name, date))
        connection.commit()
