import random
from Spieler import SpielerKlasse
from Deck import Deck
from Stich import Stich


def spiel(Spieler):

    # Ausfuchsen wer gibt
    geber = random.choice(range(4))
    Spieler[geber].set_geber(True)

    dran = (geber + 1) % 4

    # Spieler der "dran" ist, definiert das Spiel

    Spielfarbe = Spieler[dran].spielen_auf()
    if not Spielfarbe:
        print(
            "{Spieler[(dran)]}} - kein Rufspiel möglich für Spieler {Spieler[(geber+1)%4].name}, siehe Karten {Spieler[(geber+1)%4].karten}"
        )
    dran += 1

    # Definieren der Teams
    Spieler[(geber + 1) % 4].set_dran(dran)

    for i in Spieler:
        Spieler[i].Spielfarbe = Spielfarbe

        if Spieler[i].hat_Karte(Spielfarbe, "Ass"):
            Spieler[i].ist_spieler = True
            Mitspieler_Nummer = i

    print(
        f"{Spieler[(geber+1)%4].name} [kommt raus] und "
        f"{Spieler[Mitspieler_Nummer].name} "
        f"sind Spieler auf die {Spielfarbe}-Ass"
    )

    for Stich_Nummer in range(8):
        Gewinner = stich(Spieler, dran)
        dran = Gewinner.nummer
    return Spieler


def stich(Spieler, erster):
    stich = Stich()

    # wer auch immer "dran" ist, kommt raus und kann irgendeine Karte spielen
    for i in range(4):
        dran = (erster + i) % 4
        stich.Karte_reinlegen(Spieler[dran].spielt_Karte(stich), Spieler[dran])

    print(stich)

    Gewinner = stich.Gewinner()

    # Punkte für den Gewinner
    Gewinner.Stiche.append(stich)

    return Gewinner


def main():
    deck = Deck()
    deck.mischen()

    Spieler = {}
    namen = ["Hans", "Sepp", "Domi", "Brucki"]
    random.shuffle(namen)
    for i in range(4):
        Spieler[i] = SpielerKlasse(i, namen.pop())
        Spieler[i].get_karten(deck.getKarten())

    for j in Spieler:
        print(
            "%s: %s "
            % (Spieler[j].name, ", ".join([str(karte) for karte in Spieler[j].karten]))
        )

    spiel(Spieler)

    # wer hat gewonnen?
    for i in Spieler:
        print("%s: %s Punkte" % (Spieler[i].name, Spieler[i].get_punkte()))

    Spieler_Punkte = 0
    spielende_spieler = []
    nicht_spielende_spieler = []
    for s in Spieler.values():
        if s.ist_spieler:
            spielende_spieler.append(s)
            Spieler_Punkte += s.get_punkte()
        else:
            nicht_spielende_spieler.append(s)

    if Spieler_Punkte > 60:
        print(
            "Spieler (%s, %s) gewinnen mit %d Punkten"
            % (spielende_spieler[0].name, spielende_spieler[1].name, Spieler_Punkte)
        )
    else:
        print(
            "Nicht-Spieler (%s, %s) gewinnen mit %d Punkten"
            % (
                nicht_spielende_spieler[0].name,
                nicht_spielende_spieler[1].name,
                120 - Spieler_Punkte,
            )
        )


main()
