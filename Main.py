import random
from typing import List

from Game_Environment import Gamestate
from Player import Players
from Deck import Deck
from Trick import Trick


def next_turn(game_state) -> int:
    game_state.current_turn = (game_state.current_turn + 1) % 4
    return game_state.current_turn


def set_turn(game_state, position_to_set) -> None:
    game_state.current_turn = game_state.players[position_to_set].number
    return None


def define_game(game_state):
    # Find out who starts?
    set_turn(game_state=game_state, position_to_set=random.randint(0, 3))
    starting_player = game_state.players[game_state.current_turn]

    # We only allow Rufspiel atm
    game_state.game_type = 'normal'

    # Starting player can define the game
    color_of_the_game = None
    for _ in range(4):
        color_of_the_game = starting_player.spielen_auf()
        if color_of_the_game:
            game_state.called_ace = color_of_the_game
            game_state.teams['ist_spieler'].append(starting_player.number)
            starting_player.ist_spieler = True
            print(f"{starting_player.name} spielt auf {color_of_the_game}-Ass")
            break
        if not color_of_the_game:
            print(
                f"Kein Rufspiel möglich für Spieler {starting_player.name}, "
                f"siehe Karten: {[card.__str__() for card in starting_player.karten]}"
            )
            starting_player = next_turn(game_state)

    # ATM we start a new game if no one can play a Rufspiel
    if not color_of_the_game:
        game_state.game_phase = 5
        return game_state

    return game_state


def play(game_state) -> Gamestate:
    # Start to find out what to play
    game_state.game_phase = 1

    # Define the game we are going to play
    game_state = define_game(game_state=game_state)

    # Now we tell every player what game we play
    for player in game_state.players.values():
        player.colour_of_the_game = game_state.called_ace

    # Define the teams - identify the teammate of the starting player and tell only him
    teammate_of_starting_player = [
        player.number for player in game_state.players.values() if player.hat_Karte(
            game_state.called_ace, "Ass")][0]
    game_state.players[teammate_of_starting_player].ist_spieler = True

    print(
        f"{game_state.players[game_state.current_turn].name} kommt raus und "
        f"{game_state.players[teammate_of_starting_player].name} "
        f"sind Spieler auf die {game_state.called_ace}-Ass"
    )

    # The others know that they are nicht_spieler
    for player in game_state.players.values():
        if player.number not in (game_state.current_turn, teammate_of_starting_player):
            player.ist_nicht_spieler = True

    # Now let's play that game
    game_state.game_phase = 2

    for trick_number in range(8):
        # Play the trick
        game_state = play_game_trick(game_state=game_state)
        winner_of_the_trick = game_state.played_tricks[trick_number].winner().number
        set_turn(game_state=game_state, position_to_set=winner_of_the_trick)

    # After 8 rounds, we know who won the game
    if game_state.points['ist_spieler'] > 60:
        game_state.winner = game_state.teams['ist_spieler']
    else:
        game_state.winner = game_state.teams['nicht_spieler']

    game_state.game_phase = 3

    return game_state


def play_game_trick(game_state) -> Gamestate:
    trick = Trick()

    # Whose turn it is can start the trick
    for _ in game_state.players:
        card = game_state.players[game_state.current_turn].spielt_Karte(trick)

        # When called ace is played, everyone knows the teams
        if card.farbe == game_state.called_ace and card.schlag == "Ass":
            game_state.teams['ist_spieler'].append(game_state.current_turn)
            for player in game_state.players.values():
                if player.number not in game_state.teams['ist_spieler']:
                    game_state.teams['nicht_spieler'].append(player.number)

        trick.Karte_reinlegen(card, game_state.players[game_state.current_turn])
        game_state.current_trick = trick
        next_turn(game_state=game_state)

    # Update data
    game_state.played_tricks[len(game_state.played_tricks)] = trick
    if trick.winner() in game_state.teams['ist_spieler']:
        game_state.points['ist_spieler'] += trick.get_punkte()
    else:
        game_state.points['nicht_spieler'] += trick.get_punkte()

    print(trick)

    # Points for the winner
    trick.winner().stiche.append(trick)

    return game_state


def main(players) -> List:
    print("\n\n Neue Runde, runde, runde, ...\n\n")

    # Reset the player's data
    for player in players.values():
        player.reset()

    # The game state is what every player can know at any given moment
    game_state = Gamestate(players=players)

    # Let's hand out the cards for that game
    deck = Deck()
    deck.shuffle()

    for player in game_state.players.values():
        player.get_karten(deck.getKarten())
        print(
            "%s: %s "
            % (player.name, ", ".join([str(card) for card in player.karten]))
        )

    # Ok, let's play the game
    play(game_state=game_state)

    return game_state.winner


# Driver code
names = ["Hans", "Sepp", "Domi", "Brucki"]
random.shuffle(names)
players = {}
for i in range(4):
    players[i] = Players(i, names.pop())

winner = main(players=players)
print(f"{players[winner[0]].name} und {players[winner[1]].name} haben gewonnen")
