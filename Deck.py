from Karte import Karte
import random


class Deck:
    def __init__(self):
        farben = ['Eichel', 'Gras', 'Herz', 'Schellen']
        schlaege = ['7', '8', '9', 'Unter', 'Ober', 'König', '10', 'Ass']
        self.deck = []
        for farbe in farben:
            for schlag in schlaege:
                self.deck.append(Karte(farbe, schlag))

    def mischen(self):
        random.shuffle(self.deck)

    def getKarten(self):
        Hand = []
        for i in range(8):
            Hand.append(self.deck.pop(0))
        return Hand
