import random


class Fiende:

    def __init__(self, navn, beskrivelse, hp, skade, blokkert_retning, belonning=None, tegning=""):
        self._navn = navn
        self._beskrivelse = beskrivelse
        self._hp = hp
        self._skade = skade
        self._blokkert_retning = blokkert_retning   # f.eks. "nord"
        self._belonning = belonning                 # en Gjenstand, eller None
        self._tegning = tegning
        

    def hent_navn(self):
        return self._navn

    def hent_beskrivelse(self):
        return self._beskrivelse

    def hent_hp(self):
        return self._hp

    def hent_blokkert_retning(self):
        return self._blokkert_retning

    def hent_belonning(self):
        return self._belonning

    def beregn_skade(self):
        return max(self._skade + random.randint(-2, 2), 1)

    def ta_skade(self, mengde):
        self._hp = max(self._hp - mengde, 0)

    def lever(self):
        return self._hp > 0

    def hent_tegning(self):
        return self._tegning