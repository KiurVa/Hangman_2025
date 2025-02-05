import glob
import os

from models.FileObject import FileObject
from models.Leaderboard import Leaderboard


class Model:
    def __init__(self):
        self.__images_files = [] #Tühi list piltide jaoks
        self.load_image('images')
        self.__file_object = FileObject('databases', 'words.txt')
        self.__categories = self.__file_object.get_unique_categories() #Unikaalsed kategooriad
        #print(self.__file_object.get_random_word(None)) #Kontroll, et tagastab suvalisi sõnu
        self.__scoreboard = Leaderboard() #loob edetabli objekti

    def load_image(self, folder):
        if not os.path.exists(folder): #Kontrollime kas kaust on olemas
            raise FileNotFoundError(f'Kausta {folder} ei ole.')
        images = glob.glob(os.path.join(folder, '*.png')) #Kaustast kõik png laiendiga failid
        if not images:
            raise FileNotFoundError(f'Kaustas {folder} ei ole PNG laiendiga faile.')
        self.__images_files = images

    #GETTERS
    @property
    def image_files(self): #Tagastab piltide listi
        return self.__images_files

    @property
    def categories(self): #tagastab kategooriate listi
        return self.__categories