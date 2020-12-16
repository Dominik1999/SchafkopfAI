class Stich:
    def __init__(self):
        self.Spielfarbe = None
        self.data = []

    def is_bicked(self):
        return True

    def Karte_reinlegen(self, karte, Spieler):

        self.data.append({'karte': karte, 'spieler': Spieler})

        #self.spieler[Spieler.nummer] = Spieler

        if not self.Spielfarbe:
            self.Spielfarbe = karte.wirkliche_Farbe()
        #self.karten[Spieler.nummer] = karte

    def Gewinner(self):
        tmp = sorted(self.data, key=lambda x: x['karte'].get_Werte() + (0.5 if x['karte'].farbe == self.Spielfarbe else 0), reverse=True)
        return tmp[0]['spieler']

    def __str__(self):
        return "%s (Gewinner: %s)" % (
            ", ".join(["%s: %s" % (x['spieler'].name, x['karte']) for x in self.data]),
            self.Gewinner().name
        )

    def get_punkte(self):
        return sum([x['karte'].get_Punkte() for x in self.data])
