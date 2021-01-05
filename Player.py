import random


class Players:
    def __init__(self, number, name):
        self.name = name
        self.number = number
        self.ist_spieler = False
        self.dran = False
        self.colour_of_the_game = None
        self.stiche = []
        self.karten = []

    def get_punkte(self):
        return sum([stich.get_punkte() for stich in self.stiche])

    def get_karten(self, karten):
        self.karten = karten

    def hat_Karte(self, farbe, schlag):
        for karte in self.karten:
            if karte.ist_karte(farbe, schlag):
                return True
        return False

    def __moegliche_Rufsau_Farben(self):
        moegliche_farben = {
            "Schellen": False,
            "Eichel": False,
            "Gras": False,
        }
        for karte in self.karten:
            if karte.ist_Trumpf():
                continue
            moegliche_farben[karte.farbe] = True
        for farbe in moegliche_farben.keys():
            if self.hat_Karte(farbe, "Ass"):
                moegliche_farben[farbe] = False
        return list(filter(moegliche_farben.get, moegliche_farben))

    def spielen_auf(self):
        possible_colors = self.__moegliche_Rufsau_Farben()
        if len(possible_colors) == 0:
            return None
        # TODO AI einfügen
        color_of_the_game = random.choice(possible_colors)
        return color_of_the_game

    def hat_wirkliche_Farbe(self, farbe):
        for karte in self.karten:
            if karte.wirkliche_Farbe() is farbe:
                return True
        return False

    def __moegliche_Spielkarten(self, stich):
        # der erste darf alles spielen,...
        if not stich.Spielfarbe:
            # ... sofern er nicht die Rufsau hat
            if not self.hat_Karte(self.colour_of_the_game, "Ass"):
                return self.karten

            # ... hat er die Rufsau, darf er weglaufen, falls er >3x Farbe hat
            elif sum(self.colour_of_the_game == karte.wirkliche_Farbe() for karte in self.karten) > 3:
                return self.karten

            # ... ist das nicht der Fall, darf er nur nicht selbst suchen
            else:
                return list(
                    karte
                    for karte in self.karten
                    if (karte.wirkliche_Farbe() != self.colour_of_the_game or karte.schlag == "Ass")
                )

        if not self.hat_wirkliche_Farbe(stich.Spielfarbe):
            return self.karten

        return list(
            karte
            for karte in self.karten
            if karte.wirkliche_Farbe() is stich.Spielfarbe
        )
        # Trumpf ist auch eine Spielfarbe

    def spielt_Karte(self, stich):
        # TODO ersetzen durch AI
        Spielkarte = random.choice(self.__moegliche_Spielkarten(stich))
        for karte in self.karten:
            if karte.ist_karte(Spielkarte.farbe, Spielkarte.schlag):
                self.karten.remove(Spielkarte)
        return Spielkarte

    def reset(self):
        self.ist_spieler = False
        self.dran = False
        self.colour_of_the_game = None
        self.stiche = []
        self.karten = []
