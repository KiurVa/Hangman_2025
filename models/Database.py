import os
import sqlite3


class Database:
    db_name = os.path.join('databases', 'hangman_2025.db')

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()
        self.check_tables()


    def connect(self):
        if not os.path.exists(self.db_name):
            raise FileNotFoundError('Andmebaasi ei ole. Rakendus ei käivitu.')
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f'Ühendus andmebaasiga {self.db_name} on loodud.')
        except sqlite3.Error as e:
            raise Exception(f'Tõrge andmebaasi ühenduse loomisel: {e}')

    def check_tables(self):
        self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="words";')
        if not self.cursor.fetchone():
            raise FileNotFoundError('Tabel words puudub. Rakendus ei käivitu.')

        self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="leaderboard";')
        if not self.cursor.fetchone():
            self.create_leaderboard_table()

    def create_leaderboard_table(self):
        leaderboard = """
        CREATE TABLE leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            word TEXT,
            letters TEXT,
            game_length INTEGER,
            game_time TEXT
        );
        """
        self.cursor.execute(leaderboard)
        self.conn.commit()
        print('Tabel leaderboard on loodud.')



    def close_connection(self):
        if self.conn:
            self.conn.close()
            print(f'Ühendus andmebaasiga {self.db_name} suletud.')

