import os
import sqlite3
from datetime import datetime
from random import random

from views.View import View


class Database:
    db_name = os.path.join('databases', 'hangman_2025.db')

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()
        self.check_tables()
        #self.read_leaderboard()


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

        self.cursor.execute('SELECT * FROM words;')
        if not self.cursor.fetchone():
            raise ValueError('Tabel words on tühi. Rakendus ei käivitu.')

        self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="leaderboard";')
        if not self.cursor.fetchone():
            self.create_leaderboard_table()

    def create_leaderboard_table(self):
        leaderboard = """
        CREATE TABLE leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, NOT NULL,
            word TEXT NOT NULL,
            letters TEXT NOT NULL,
            game_length INTEGER NOT NULL,
            game_time TEXT NOT NULL,
        );
        """
        self.cursor.execute(leaderboard)
        self.conn.commit()
        print('Tabel leaderboard on loodud.')

    def get_unique_categories(self):
        self.cursor.execute('SELECT DISTINCT category FROM words;')
        categories = [row[0] for row in self.cursor.fetchall()]
        categories.sort()
        categories.insert(0, 'Vali kategooria')
        return [category.capitalize() for category in categories]

    def get_random_word(self, category):
        if category is None:
            self.cursor.execute('SELECT word FROM words order by RANDOM() LIMIT 1;')
            word = self.cursor.fetchone()[0]
            return word
        else:
            category = category.lower()
            self.cursor.execute('SELECT word FROM words Where category=? ORDER BY RANDOM() LIMIT 1;', (category,))
            word = self.cursor.fetchone()[0]
            return word

    def read_leaderboard(self):
        self.cursor.execute('SELECT * FROM leaderboard;')
        data = self.cursor.fetchall()
        return data

    def save_player_score(self, name, word, letters, game_length):
        game_time = datetime.now().strftime('%Y-%m-%d %T')
        if not name.strip():
            name = random.choice(['Teadmata', 'Tundmatu', 'Unknown'])
        self.cursor.execute("""
        INSERT INTO leaderboard (name, word, letters, game_length, game_time)
        VALUES (?, ?, ?, ?, ?);
        """, (name.strip(), word, letters, game_length, game_time))
        self.conn.commit()



    def close_connection(self):
        if self.conn:
            self.conn.close()
            print(f'Ühendus andmebaasiga {self.db_name} suletud.')

