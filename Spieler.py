import random


class SpielerKlasse:
    def __init__(self, nummer, name):
        self.name = name
        self.nummer = nummer
        self.ist_spieler = False
        self.Stiche = []

    def get_punkte(self):
        return sum([stich.get_punkte() for stich in self.Stiche])

    def get_karten(self, karten):
        self.karten = karten

    def set_geber(self, ist_geber):
        self.Geber = ist_geber

    def set_dran(self, dran):
        self.dran = dran

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
        farben = self.__moegliche_Rufsau_Farben()
        if len(farben) == 0:
            return None
        # TODO AI einfügen
        return random.choice(farben)

    def hat_wirkliche_Farbe(self, farbe):
        for karte in self.karten:
            if karte.wirkliche_Farbe() is farbe:
                return True
        return False

    def __moegliche_Spielkarten(self, stich):
        # der erste darf alles spielen,...
        if not stich.Spielfarbe:
            # ...außer selbst suchen, wenn er <4 der Farbe und die Rufsau hat
            if not self.hat_Karte(self.Spielfarbe, "Ass"):
                return self.karten
            return list(
                karte
                for karte in self.karten
                if karte.wirkliche_Farbe() != self.Spielfarbe or karte.schlag is "Ass"
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
