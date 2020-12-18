import random
from Spieler import SpielerKlasse
from Deck import Deck
from Stich import Stich


def next_turn(players) -> int:
    turn = whos_turn(players)
    players[turn].dran = False
    next_player = (turn + 1) % 4
    players[next_player].dran = True
    return next_player


def set_turn(players, position_to_set) -> None:
    for player in players:
        players[player].dran = False

    players[position_to_set].dran = True
    return None


def whos_turn(players) -> int:
    turn = [number for number in players if players[number].dran is True]
    if len(turn) > 1:
        print(len)
        breakpoint()
    if turn:
        return turn[0]
    return None


def play(players):

    # Who starts?
    set_turn(players=players, position_to_set=random.randint(0, 3))
    starting_player = whos_turn(players=players)

    # Who's turn it is, can define the game
    for i in range(4):
        colour_of_that_game = players[starting_player].spielen_auf()
        if colour_of_that_game:
            players[starting_player].ist_spieler = True
            print(f"{players[starting_player].name} spielt auf {colour_of_that_game}-Ass")
            break
        if not colour_of_that_game:
            print(
                f"Kein Rufspiel möglich für Spieler {players[starting_player].name}, "
                f"siehe Karten: {[karte.__str__() for karte in players[starting_player].karten]}"
            )
            starting_player = next_turn(players)

    # ATM we start a new game if no one can play a Rufspiel
    if not colour_of_that_game:
        return main()

    # Now we tell every player what game we play (TODO add class game that
    # consists of 8 game tricks)
    for player in players:
        players[player].colour_of_the_game = colour_of_that_game

    # Define the teams - identify the teammate of the starting player
    teammate_of_starting_player = [
        player for player in players if players[player].hat_Karte(
            colour_of_that_game, "Ass")][0]
    players[teammate_of_starting_player].ist_spieler = True

    print(
        f"{players[starting_player].name} [kommt raus] und "
        f"{players[teammate_of_starting_player].name} "
        f"sind Spieler auf die {colour_of_that_game}-Ass"
    )

    # now let's play that game
    for _ in range(8):
        winner_of_the_trick = play_game_trick(players=players)
        set_turn(players=players, position_to_set=winner_of_the_trick.nummer)

    # after 8 rounds, who is the winner?
    playing_team = [player.nummer for player in players.values()
                    if player.ist_spieler is True]
    non_playing_team = [
        player.nummer for player in players.values() if player.ist_spieler is False]

    assert len(playing_team) == 2
    assert len(non_playing_team) == 2

    winning_team_of_the_game = playing_team if sum(
        players[player].get_punkte() for player in playing_team) > 60 else non_playing_team

    return winning_team_of_the_game


def play_game_trick(players) -> SpielerKlasse:
    stich = Stich()

    # wer auch immer "dran" ist, kommt raus und kann irgendeine Karte spielen
    for _ in players:
        stich.Karte_reinlegen(players[whos_turn(players)].spielt_Karte(
            stich), players[whos_turn(players)])
        next_turn(players)

    print(stich)

    winner_of_the_trick = stich.winner()

    # Punkte für den Gewinner
    winner_of_the_trick.stiche.append(stich)

    return winner_of_the_trick


def main():
    deck = Deck()
    deck.mischen()

    players = {}
    names = ["Hans", "Sepp", "Domi", "Brucki"]
    random.shuffle(names)

    for i in range(4):
        players[i] = SpielerKlasse(i, names.pop())
        players[i].get_karten(deck.getKarten())

    print("\n\n Neue Runde, runde, runde, ...\n\n")
    for j in players:
        print(
            "%s: %s "
            % (players[j].name, ", ".join([str(karte) for karte in players[j].karten]))
        )

    winning_team_of_the_game = play(players)

    winner1 = winning_team_of_the_game[0]
    winner2 = winning_team_of_the_game[1]

    print(
        f'Gewinner: {players[winner1].name} und {players[winner2].name} '
        f'mit {players[winner1].get_punkte() + players[winner2].get_punkte()} Punkten!'
    )


# Driver code
for _ in range(100):
    main()
