import glob
import os
from datetime import datetime
import random

from models.Database import Database
from models.FileObject import FileObject
from models.Leaderboard import Leaderboard


class Model:
    def __init__(self):
        self.__images_files = [] #Tühi list piltide jaoks
        self.load_image('images')
        self.__file_object = Database()
        self.__categories = self.__file_object.get_unique_categories() #Unikaalsed kategooriad
        #print(self.__file_object.get_random_word(None)) #Kontroll, et tagastab suvalisi sõnu
        self.__scoreboard = Database() #loob edetabli objekti
        self.titles = ['Poomismäng 2025', 'Kas jäid magama', 'Ma ootan su käiku', 'Sisesta juba see täht',
                       'Sisesta juba see täht', 'Zzzzzz.....']

        #Mängu muutujad
        self.__new_word = None #juhusliku sõna jaoks
        self.__user_word = [] #Kasutaja leitud sõnad
        self.__counter = 0 #Vigade loendur
        self.__all_user_chars = [] #Kõik valesti sisestatud tähed

    def load_image(self, folder):
        if not os.path.exists(folder): #Kontrollime kas kaust on olemas
            raise FileNotFoundError(f'Kausta {folder} ei ole.')
        images = glob.glob(os.path.join(folder, '*.png')) #Kaustast kõik png laiendiga failid
        if not images:
            raise FileNotFoundError(f'Kaustas {folder} ei ole PNG laiendiga faile.')
        self.__images_files = images

    def start_new_game(self, category_id, category):
        if category_id == 0:
            category = None
        self.__new_word = self.__file_object.get_random_word(category) #Juhuslik sõna
        self.__user_word = [] #Algseis
        self.__counter = 0 #Algseis
        self.__all_user_chars = [] #Algseis

        #asenda sõnas kõik tähed allkriipsuga M A J A => _ _ _ _
        for i in range(len(self.__new_word)):
            self.__user_word.append('_')
        print(self.__new_word, self.__user_word)

    def get_user_input(self, user_input):
        #User_input on sisestuskasti kirjutatud märk
        if user_input:
            user_char = user_input[:1] #Esimene märk sisestusest
            if user_char.lower() in self.__new_word.lower():
                self.change_user_input(user_char) #Leiti täht
            else: #Ei leitud tähte
                self.__counter += 1
                self.__all_user_chars.append(user_char.upper())


    def change_user_input(self, user_char):
        #Asenda kõik allkriipsud tähega
        current_word = self.char_to_list(self.__new_word)
        x = 0
        for c in current_word:
            if c.lower() == user_char.lower():
                self.__user_word[x] = user_char.upper()
            x += 1

    @staticmethod
    def char_to_list(word):
        #String to List
        chars = []
        chars[:0] = word
        return chars

    def get_all_user_chars(self):
        return ', '.join(self.__all_user_chars) #List tehakse komaga eraldatud stringiks

    def read_leaderboard(self):
        return self.__file_object.read_leaderboard()

    def save_player_score(self, name, seconds):
        self.__scoreboard.save_player_score(name, self.__new_word, self.get_all_user_chars(), seconds)
        """today = datetime.now().strftime('%Y-%m-%d %T')
        if not name.strip():
            name = random.choice(['Teadmata', 'Tundmatu', 'Unknown'])
        with open(self.__scoreboard.file_path, 'a', encoding='utf-8') as f:
            line = ';'.join([name.strip(), self.__new_word, self.get_all_user_chars(), str(seconds), today])
            f.write(line + '\n')"""

    #GETTERS
    @property
    def image_files(self): #Tagastab piltide listi
        return self.__images_files

    @property
    def categories(self): #tagastab kategooriate listi
        return self.__categories

    @property
    def user_word(self): #tagastab kasutaja leitud tähed
        return self.__user_word

    @property
    def counter(self): #tagastab vigade arvu
        return self.__counter