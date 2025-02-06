import os.path

from models.Score import Score


class Leaderboard:
    def __init__(self):
        self.__file_path = os.path.join('databases', 'leaderboard.txt')
        self.check_file() #Kontrollib faili olemasolu ja kui pole, siis tee

    def check_file(self):
        if not os.path.exists(self.__file_path):
            self.create_leaderboard() #Uus meetod, sest nimi ütleb kontrollb faili olemasolu

    def create_leaderboard(self):
        header = ['name', 'word', 'letters', 'game lenght', 'game time']
        with open(self.__file_path, 'a', encoding='utf-8') as f:
            f.write(';'.join(header) + '\n')

    def read_leaderboard(self):
        leaderboard = []
        with open(self.__file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines() #Kõik read listi

            if not lines:
                return[] #Tagastatakse tühi list
            for line in lines[1:]: #Alates teisest reas
                line = line.strip() #Korrastame rea
                name, word, letters, game_lenght, game_time = line.split(';')
                leaderboard.append(Score(name, word, letters, int(game_lenght), game_time))
            leaderboard = sorted(leaderboard, key=lambda x: (x.game_length, len(x.letters.split(', ')))) #Sorteerida kestvuse järgi

        return leaderboard

    @property
    def file_path(self):
        return self.__file_path #failinimi koos kausataga database/leaderboar.txt
