import os
import random


class FileObject:

    def __init__(self, folder, filename):
        path = os.path.join(folder, filename) #Paneb kausta ja faili kokku (databases/words.txt)
        self.__data = self._read_file(path) #Kogu faili sisu tuleb siia {}

    @staticmethod
    def _read_file(path):
        if not os.path.exists(path):
            raise FileNotFoundError(f'Faili {path} ei leitud.')

        data = {} #Dictionary
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            if not lines:
                raise ValueError(f'Fail {path} on tühi.')

            #Esimene rida on päis
            header = lines[0].strip().split(';') #['word', 'categry']
            if len(header) != 2:
                raise ValueError('Faili formaat on vale.')

            #Loeb ülejäänud reas
            for line in lines[1:]:
                word, category = line.strip().split(';')
                if category not in data:
                    data[category] = [] #Lisab tühja kategooria listina
                data[category].append(word) #Lisab sõna kategooriasse
        return data #tagasta faili sisu - {'hoone': ['suvila', 'kasvuhoone'], 'amet': ['lasteaiakasvataja', 'bussijuht']}

    def get_unique_categories(self):
        categories = list(self.__data.keys()) #tagastab ['hoone', 'amet']
        categories.sort() #Sroteerib tähestikku

        #Lisa "Vali kategooria listi esimeseks elemendiks"
        categories.insert(0, 'Vali kategooria')
        #categories = ['Vali kategooria'] + categories
        return [category.capitalize() for category in categories] #tagatsab kategooriad, esimene täht suurena

    def get_random_word(self, category):
        if category is None: #kategooriat ei ole valitud
            all_words = [word for words in self.__data.values() for word in words] #tagastab kõik sõnad
            return random.choice(all_words) if all_words else None #tagastab suvalise sõna

        category = category.lower() #Argument muudetakse väikseks täheks!!
        if category in self.__data:
            return random.choice(self.__data[category]) if self.__data[category] else None

        #Kui kategooriat ei leitud
        return None