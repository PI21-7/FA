import sqlite3

from typing import List, Tuple


class Connections(object):
    database = 'FA.db'

    @staticmethod
    def safe(func):
        def inside(*args, **kwargs):
            with sqlite3.connect(Connections.database) as connection:
                result = func(*args, connection=(connection, connection.cursor()), **kwargs)
            return result
        return inside


class Database(object):

    @Connections.safe
    def all_users(self, connection):
        connection, cursor = connection
        cursor = cursor.execute(
            '''SELECT ALL chat_id FROM Users'''
        )
        connection.commit()
        return cursor.fetchall()

    @Connections.safe
    def add_user(self, connection: tuple, chat_id: str, user_group: str, username: str):
        connection, cursor = connection
        cursor = cursor.execute('''SELECT user_group FROM Users WHERE chat_id = ?''', (chat_id,))
        if cursor.fetchall():
            cursor.execute('''UPDATE Users SET user_group = ? WHERE chat_id = ?;''', (user_group, chat_id))
        else:
            cursor.execute('''INSERT INTO Users (chat_id, user_group, username) VALUES (?, ?, ?)''',
                           (chat_id, user_group.upper(), username))

        return connection.commit()

    @Connections.safe
    def get_user_group(self, connection: tuple, chat_id: str) -> str:
        connection, cursor = connection
        cursor = cursor.execute('''SELECT user_group FROM Users WHERE chat_id = ?''', (chat_id,)).fetchall()
        connection.commit()
        return cursor

    @Connections.safe
    def init(self, connection: tuple) -> None:
        connection, cursor = connection
        print('Creating "Homework" Table...')
        cursor.execute(
            f'create table if not exists Homework('
            f'id         INTEGER primary key,'
            f'subject_id int  not null,'
            f'date       text not null,'
            f'text       text not null,'
            f'"Group"    text not null,'
            f'Author     text not null)'
        )
        print('Creating "Files" Table...')
        cursor.execute('''
        create table if not exists Files
        (
            id         INTEGER primary key,
            Data       TEXT,
            filename   TEXT,
            group_name TEXT
        );
        ''')
        print('Creating "Users" Table...')
        cursor.execute('''create table if not exists Users (
        id          INTEGER primary key,
        chat_id     TEXT not null,
        user_group  TEXT not null,
        username  TEXT not null
        )''')
        print('Creating "Materials" Table...')
        cursor.execute('''
        create table if not exists Materials
        (
            id         INTEGER primary key,
            file_id   TEXT,
            group_name TEXT,
            file_name TEXT
        );
        ''')

        return connection.commit()

    @Connections.safe
    def attach_file_materials(self, connection: tuple, file_id: str, group: str, file_name: str):
        connection, cursor = connection

        cursor.execute('''INSERT INTO Materials (FILE_ID, GROUP_NAME, FILE_NAME) VALUES (?, ?, ?)''', (file_id, group, file_name,))
        return connection.commit()

    @Connections.safe
    def delete_material(self, connection: tuple, group: str, file_id: str):
        connection, cursor = connection

        cursor.execute('''DELETE FROM Materials WHERE file_id = ? AND group_name = ?;''', (file_id, group))
        return connection.commit()

    @Connections.safe
    def is_file_attached_materials(self, connection: tuple, group: str, file_name: str):
        connection, cursor = connection
        cursor = cursor.execute('''SELECT file_id FROM Materials WHERE group_name = ? AND file_name = ?''', (group, file_name,))
        if cursor.fetchall():
            return False
        return True

    @Connections.safe
    def get_attachments_materials(self, connection: tuple, group: str):
        connection, cursor = connection
        cursor = cursor.execute('''SELECT ALL file_id FROM Materials WHERE group_name = ?''', (group,))
        connection.commit()
        return cursor.fetchall()

    @Connections.safe
    def attach_file(self, connection: tuple, date: str, filename: str, group: str):
        connection, cursor = connection

        cursor.execute('''INSERT INTO Files (DATA, FILENAME, GROUP_NAME) VALUES (?, ?, ?)''', (date, filename, group))
        return connection.commit()

    @Connections.safe
    def is_file_attached(self, connection: tuple, date: str, group: str):
        connection, cursor = connection
        cursor = cursor.execute('''SELECT filename FROM Files WHERE Data = ? AND  group_name = ?''', (date, group))
        if cursor.fetchall():
            return True
        return False

    @Connections.safe
    def add_homework(self, connection: tuple, subject_name: str,
                     text: str, date: str, username: str, group: str, edit: bool = False) -> str:
        connection, cursor = connection
        # Записываем
        cursor.execute('''INSERT INTO Homework (subject_id, date, text, "Group", Author) VALUES (?, ?, ?, ?, ?)''',
                       (subject_name, date, text, group, username))
        connection.commit()
        return 'Домашнее задание добавлено' if not edit else "Домашнее задание изменено"

    @Connections.safe
    def is_available_homework_by_date(self, connection: tuple, date: str, group: str, data=False):
        connection, cursor = connection
        cursor = cursor.execute('''SELECT subject_id, text FROM Homework WHERE date = ? AND "Group" = ?''',
                                (date, group)).fetchall()
        connection.commit()
        if data:
            return cursor

        if cursor:
            return True
        return False

    @Connections.safe
    def is_exists(self, connection: tuple, subject_name: str, date: str, group: str):
        connection, cursor = connection
        cursor = cursor.execute(
            '''SELECT subject_id AND date FROM Homework WHERE subject_id = ? AND date = ? AND "Group" = ?''',
            (subject_name, date, group)).fetchall()
        connection.commit()
        if cursor:
            return True
        return False

    @Connections.safe
    def receive_homework(self, connection: tuple, subject_name: str, date: str, group: str) -> str or List[Tuple[str]]:
        connection, cursor = connection
        answer = cursor.execute(
            '''SELECT text FROM Homework WHERE subject_id = ? AND date = ? AND "Group" = ?''',
            (subject_name, date, group)).fetchall()
        connection.commit()
        if not answer:
            return answer
        return answer[0][0]

    @Connections.safe
    def get_attachments(self, connection: tuple, date: str, group: str):
        connection, cursor = connection
        cursor = cursor.execute('''SELECT ALL filename FROM Files WHERE Data = ? AND group_name = ?''', (date, group))
        connection.commit()
        return cursor.fetchall()

    @Connections.safe
    def edit_homework(self, connection: tuple, subject_name: str, date: str, text: str, group: str):
        connection, cursor = connection
        cursor.execute(
            '''UPDATE Homework SET text = ? WHERE subject_id = ? AND date = ? AND "Group" = ?;''',
            (text, subject_name, date, group)
        )
        return connection.commit()

    @Connections.safe
    def delete_homework(self, connection: tuple, subject_name: str, date: str, group: str) -> None:
        connection, cursor = connection
        cursor.execute('''
        DELETE FROM Homework WHERE subject_id = ? AND date = ? AND "Group" = ?;''', (subject_name, date, group))
        return connection.commit()
