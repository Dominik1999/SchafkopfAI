class Karte:
    def __init__(self, farbe, schlag):
        self.farbe = farbe
        self.schlag = schlag

    def get_Punkte(self):
        if self.schlag == '7':
            return 0
        if self.schlag == '8':
            return 0
        if self.schlag == '9':
            return 0
        if self.schlag == 'Unter':
            return 2
        if self.schlag == 'Ober':
            return 3
        if self.schlag == 'König':
            return 4
        if self.schlag == '10':
            return 10
        if self.schlag == 'Ass':
            return 11

    def get_Farbewert(self):
        if self.farbe == 'Eichel':
            return 4
        if self.farbe == 'Gras':
            return 3
        if self.farbe == 'Herz':
            return 2
        if self.farbe == 'Schellen':
            return 1

    def wirkliche_Farbe(self):
        if self.ist_Trumpf():
            return 'Trumpf'
        return self.farbe

    def ist_Trumpf(self):
        if self.schlag in ('Ober', 'Unter'):
            return True
        elif self.farbe is 'Herz':
            return True
        return False

    def get_Werte(self):
        if self.schlag == 'Ober':
            return 16 + self.get_Farbewert()
        if self.schlag == 'Unter':
            return 12 + self.get_Farbewert()
        if self.farbe is 'Herz':
            herzaufschlag = 6
        else:
            herzaufschlag = 0
        if self.schlag == 'Ass':
            return 6 + herzaufschlag
        if self.schlag == '10':
            return 5 + herzaufschlag
        if self.schlag == 'König':
            return 4 + herzaufschlag
        if self.schlag == '9':
            return 3 + herzaufschlag
        if self.schlag == '8':
            return 2 + herzaufschlag
        if self.schlag == '7':
            return 1 + herzaufschlag

    def __str__(self):
        return f"{self.farbe}-{self.schlag}"

    def ist_karte(self, farbe, schlag):
        return (self.farbe is farbe and self.schlag is schlag)