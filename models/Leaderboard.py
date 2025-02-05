import os.path


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
