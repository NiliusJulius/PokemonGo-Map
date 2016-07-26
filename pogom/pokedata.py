import csv

from base64 import b64encode
from datetime import datetime

class Pokedata:
    pokedata = None
    @staticmethod
    def get(pokemon_id):
        if not Pokedata.pokedata:
            Pokedata.pokedata = {}
            with open('pokedata.csv', 'rU') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    id = int(row[0])
                    name = row[1]
                    rarity = int(row[2])
                    Pokedata.pokedata[id] = {
                        'name': name,
                        'rarity': rarity
                    }
        return Pokedata.pokedata[pokemon_id]