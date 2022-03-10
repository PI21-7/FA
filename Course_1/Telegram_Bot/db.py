import sqlite3

from typing import List, Tuple, Final


class Connections(object):
    def __init__(self, database: str = 'Homework.db') -> None:
        self.database: Final = database

    @staticmethod
    def safe(func):
        def inside(*args, **kwargs):
            with sqlite3.connect('Homework.db') as connection:
                result = func(*args, connection=(connection, connection.cursor()), **kwargs)
                return result

        return inside


class Database(object):

    @Connections.safe
    def init(self, connection: tuple) -> None:
        connection, cursor = connection
        cursor.execute(
            ''' 
        create table if not exists Homework
        (   id         INTEGER primary key,
            subject_id int  not null,
            date       text not null,
            text       TEXT not null
        )
            '''
        )

        connection.commit()

    @Connections.safe
    def add_homework(self, connection: tuple, subject_name: str, text: str, date: str) -> str:
        is_added = self.receive_homework(subject_name=subject_name, date=date)
        subject_name = subject_name.lower()
        if is_added:
            return 'Запись уже присутствует'
        connection, cursor = connection
        # Записываем
        cursor.execute('''INSERT INTO Homework (subject_id, date, text) VALUES (?, ?, ?)''', (subject_name, date, text))
        connection.commit()
        return 'Домашнее задание добавлено'

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
    def delete_homework(self, connection: tuple, subject_name, date) -> None:
        connection, cursor = connection
        cursor.execute('''
        DELETE FROM Homework WHERE subject_id = ? and date = ?;''', (subject_name, date))
