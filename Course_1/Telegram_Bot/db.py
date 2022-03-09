import sqlite3


class Connections(object):
    @staticmethod
    def safe(func):
        def inside(*args, **kwargs):
            with sqlite3.connect('Homework.db') as connection:
                result = func(*args, connection=(connection, connection.cursor()), **kwargs)
                return result

        return inside


class Database(object):

    @Connections.safe
    def init(self, connection):
        connection, cursor = connection
        # Создаем БД
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
    def add_message(self, connection, subject_name: str, text: str, date: str) -> None:
        connection, cursor = connection
        subject_name = subject_name.lower()
        # Записываем
        cursor.execute('''INSERT INTO Homework (subject_id, date, text) VALUES (?, ?, ?)''', (subject_name, date, text))
        connection.commit()

    @Connections.safe
    def receive_homework(self, connection, subject_name: str, date: str) -> str:
        connection, cursor = connection
        subject_name = subject_name.lower()
        answer = cursor.execute(
            '''SELECT text FROM Homework WHERE subject_id = ? and date = ? ''',
            (subject_name, date))
        connection.commit()

        return answer.fetchall()[0][0]


if __name__ == '__main__':
    DB = Database()
    DB.init()
    print(DB.receive_homework(subject_name='Алгебра', date='08.03.22'))
