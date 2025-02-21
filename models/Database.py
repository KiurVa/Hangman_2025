import os
import sqlite3
from datetime import datetime
import random


class Database:
    db_name = os.path.join('databases', 'hangman_2025.db') #Andmebaasi asukoht databases/hangman_2025.db

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()
        self.check_tables() #kontrollib tabelite olemasolu


    def connect(self):
        """Loob ühenduse andmebaasiga ja kontrollib, kas andmebaas on olemas"""
        if not os.path.exists(self.db_name):
            raise FileNotFoundError('Andmebaasi ei ole. Rakendus ei käivitu.')
        try:
            if self.conn:
                self.conn.close() #Kui ühendus, siis sulgeks
                print('Varasem ühendus suleti.')
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f'Ühendus andmebaasiga {self.db_name} on loodud.')
        except sqlite3.Error as e:
            raise Exception(f'Tõrge andmebaasi ühenduse loomisel: {e}')

    def check_tables(self):
        """Kontrollib words tabeli olemasolu"""
        self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="words";')
        if not self.cursor.fetchone():
            raise FileNotFoundError('Tabel words puudub. Rakendus ei käivitu.')
        """Kontrollib, kas words tabelis on sõnu ja kategooriad"""
        self.cursor.execute('SELECT * FROM words;')
        if not self.cursor.fetchone():
            raise ValueError('Tabel words on tühi. Rakendus ei käivitu.')
        """Kontrollib kas leaderboard tabel on olemas ja vajadusel käivitab selle tegemise"""
        self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="leaderboard";')
        if not self.cursor.fetchone():
            self.create_leaderboard_table()

    def create_leaderboard_table(self):
        """Leaderboardi tabeli loomine"""
        leaderboard = """
        CREATE TABLE leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            word TEXT NOT NULL,
            letters TEXT NOT NULL,
            game_length INTEGER NOT NULL,
            game_time TEXT NOT NULL
        );
        """
        self.cursor.execute(leaderboard)
        self.conn.commit()
        print('Tabel leaderboard on loodud.')

    def get_unique_categories(self):
        """Leiab words tabelist kõik unikaalsed kategooriad ja lisab esimeseks 'Vali Kategooria'"""
        self.cursor.execute('SELECT DISTINCT category FROM words;')
        categories = [row[0] for row in self.cursor.fetchall()]
        categories.sort()
        categories.insert(0, 'Vali kategooria')
        return [category.capitalize() for category in categories]

    def get_random_word(self, category):
        """Leiab suvalise sõna, kui kategooriat pole valitud"""
        if category is None:
            self.cursor.execute('SELECT word FROM words order by RANDOM() LIMIT 1;')
            word = self.cursor.fetchone()[0]
            return word
        #Kindla kategooria valikul leiab kategooriast suvalise sõna
        else:
            category = category.lower()
            self.cursor.execute('SELECT word FROM words Where category=? ORDER BY RANDOM() LIMIT 1;', (category,))
            word = self.cursor.fetchone()[0]
            return word

    def read_leaderboard(self):
        """Loeb leaderboardi tabelist andmed ja tagastab data"""
        try:
            self.cursor.execute('SELECT COUNT(*) FROM leaderboard;')  # Kontrollib, kas tabelis on mingeid ridu
            count = self.cursor.fetchone()[0]
            if count == 0:
                return []  # Kui ridu ei ole, tagastab tühi loend
            self.cursor.execute('SELECT * FROM leaderboard ORDER BY game_length, letters;')
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            print(f"Error reading leaderboard: {e}")
            return []

    def save_player_score(self, name, word, letters, game_length):
        """Salvestab skoori leaderboard tabelisse"""
        game_time = datetime.now().strftime('%Y-%m-%d %T')
        if not name.strip():
            name = random.choice(['Teadmata', 'Tundmatu', 'Unknown'])
        self.cursor.execute("""
        INSERT INTO leaderboard (name, word, letters, game_length, game_time)
        VALUES (?, ?, ?, ?, ?);
        """, (name.strip(), word, letters, game_length, game_time))
        self.conn.commit()

    def close_connection(self):
        """Sulgeb andmebaasi ühenduse"""
        try:
            if self.conn:
                self.conn.close()
                print(f'Ühendus andmebaasiga {self.db_name} suletud.')
        except sqlite3.Error as error:
            print(f'Tõrge ühenduse sulgemisel: {error}')


