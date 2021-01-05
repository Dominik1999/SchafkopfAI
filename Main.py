import random
from Player import Players
from Deck import Deck
from Trick import Trick


def next_turn(game_state) -> int:
    game_state['current_turn'] = (game_state['current_turn'] + 1) % 4
    return game_state['current_turn']


def set_turn(game_state, position_to_set) -> None:
    game_state['current_turn'] = game_state['players'][position_to_set].number
    return None


def whose_turn(game_state) -> int:
    return game_state['current_turn']


def define_game(players, game_state):
    # Find out who starts?
    set_turn(game_state=game_state, position_to_set=random.randint(0, 3))
    starting_player = whose_turn(game_state=game_state)

    # We only allow Rufspiel atm
    game_state['game_type'] = 'normal'

    # Starting player can define the game
    color_of_the_game = None
    for _ in range(4):
        color_of_the_game = players[starting_player].spielen_auf()
        if color_of_the_game:
            game_state['called_ace'] = color_of_the_game
            game_state['teams']['ist_spieler'].append(players[starting_player].number)
            players[starting_player].ist_spieler = True
            print(f"{players[starting_player].name} spielt auf {color_of_the_game}-Ass")
            break
        if not color_of_the_game:
            print(
                f"Kein Rufspiel möglich für Spieler {players[starting_player].name}, "
                f"siehe Karten: {[card.__str__() for card in players[starting_player].karten]}"
            )
            starting_player = next_turn(game_state)

    # ATM we start a new game if no one can play a Rufspiel
    if not color_of_the_game:
        game_state['phase'] = 3
        return game_state

    return game_state


def play(players, game_state):
    # Start to find our what to play
    game_state['phase'] = 1

    # Define the game we are going to play
    game_state = define_game(players=players, game_state=game_state)

    # Now we tell every player what game we play
    for player in players.values():
        player.colour_of_the_game = game_state['called_ace']

    # Define the teams - identify the teammate of the starting player and tell only him
    teammate_of_starting_player = [
        player for player in players if players[player].hat_Karte(
            game_state['called_ace'], "Ass")][0]
    players[teammate_of_starting_player].ist_spieler = True

    print(
        f"{players[whose_turn(game_state=game_state)].name} kommt raus und "
        f"{players[teammate_of_starting_player].name} "
        f"sind Spieler auf die {game_state['called_ace']}-Ass"
    )
    # The others know that they are nicht spieler
    for player_number in players.keys():
        if player_number not in (whose_turn(game_state=game_state), teammate_of_starting_player):
            players[player_number].ist_nicht_spieler = True

    # Now let's play that game
    game_state['phase'] = 2
    for trick_number in range(8):
        winner_of_the_trick, trick = play_game_trick(players=players, game_state=game_state)
        game_state['played_tricks'][trick_number] = trick
        set_turn(game_state=game_state, position_to_set=winner_of_the_trick.number)

    # After 8 rounds, we know who won the game
    game_state['phase'] = 4

    playing_team = [player.number for player in players.values()
                    if player.ist_spieler is True]
    non_playing_team = [
        player.number for player in players.values() if player.ist_spieler is False]

    assert len(playing_team) == 2
    assert len(non_playing_team) == 2

    winning_team_of_the_game = playing_team if sum(
        players[player].get_punkte() for player in playing_team) > 60 else non_playing_team

    return winning_team_of_the_game


def play_game_trick(players, game_state) -> (Players, Trick):
    trick = Trick()

    # Whose turn it is can start the trick
    for _ in players:
        turn = whose_turn(game_state=game_state)
        card = players[turn].spielt_Karte(trick)

        # When called ace is played, everyone knows the teams
        if card.farbe == game_state['called_ace'] and card.schlag == "Ass":
            game_state['teams']['ist_spieler'].append(turn)
            for player_number in players.keys():
                if player_number not in game_state['teams']['ist_spieler']:
                    game_state['teams']['nicht_spieler'].append(player_number)

        trick.Karte_reinlegen(card, players[turn])
        game_state['current_trick'] = trick
        next_turn(game_state=game_state)

    print(trick)

    winner_of_the_trick = trick.winner()

    # Punkte für den Gewinner
    winner_of_the_trick.stiche.append(trick)

    return winner_of_the_trick, trick


def main(players, games, round):
    print("\n\n Neue Runde, runde, runde, ...\n\n")

    # Reset the player's data
    for player in players.values():
        player.reset()

    # The game state is what every player can know at any given moment
    game_state = dict(          # change to named tuple for performance reasons
        players=players,        # players and their order
        current_turn=None,      # who's turn it is
        teams=dict(
            ist_spieler=[],
            nicht_spieler=[]
        ),                      # which teams are known at that time
        phase=None,             # 1: who plays, 2: playing, 3: terminated, 4: finalized
        game_type=None,         # normal or solo
        called_ace=None,        # color of ace that is called
        played_tricks={},       # already played tricks
        points_per_player={},   # which team and player has how many points
        current_trick={},       # what is the current trick
    )

    # Let's hand out the cards for that game
    deck = Deck()
    deck.shuffle()
    for player_number in game_state['players']:
        players[player_number].get_karten(deck.getKarten())
        print(
            "%s: %s "
            % (players[player_number].name, ", ".join([str(card) for card in players[player_number].karten]))
        )

    # Ok, let's play the game
    winning_team_of_the_game = play(players=players, game_state=game_state)

    winner1 = winning_team_of_the_game[0]
    winner2 = winning_team_of_the_game[1]

    games[round] = [players[winner1].name, players[winner2].name]
    print(
        f'Gewinner: {players[winner1].name} und {players[winner2].name} '
        f'mit {players[winner1].get_punkte() + players[winner2].get_punkte()} Punkten!'
    )


# Driver code
names = ["Hans", "Sepp", "Domi", "Brucki"]
random.shuffle(names)
players = {}
games = {}
stats = {}

for i in range(4):
    players[i] = Players(i, names.pop())

for round in range(100):
    main(players=players, games=games, round=round)

for round in games:
    for name in games[round]:
        if name not in stats.keys():
            stats[name] = 0
        stats[name] += 1

print(stats)
