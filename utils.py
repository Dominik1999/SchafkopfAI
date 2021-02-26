import numpy as np
from rules import Rules


# encodes a card using 8 (for number) + 4 (for color) bits
def two_hot_encode_card(card):
    encoding = np.zeros(12)
    encoding[card[1]] = 1
    encoding[8 + card[0]] = 1
    return encoding


# encodes a game using 3 (for gametype) + 4 (for color) bits
def two_hot_encode_game(game):
    encoding = np.zeros(7)
    if game[1] is not None:
        encoding[game[1]] = 1
    if game[0] is not None:
        encoding[3 + game[0]] = 1
    return encoding


def one_hot_encode_game(game):
    one_hot_game = np.zeros(9)
    one_hot_game[Rules().games.index(game)] = 1
    return one_hot_game


def one_hot_games(games):
    one_hot_games = np.zeros(9)
    for game in games:
        one_hot_games[Rules().games.index(game)] = 1
    return one_hot_games

def one_hot_card(card):
    single_one_hot_card = np.zeros(32)
    single_one_hot_card[Rules().cards.index(card)] = 1
    return single_one_hot_card


def one_hot_cards(cards):
    #hand = sort_hand(cards) # Maybe sort cards to get better predictions?
    enc_cards = np.zeros((8, 32))
    for card, i in zip(cards, range(8)):
        enc_cards[i] = one_hot_card(card)
    return enc_cards


def sort_hand(cards):
    sorted_cards = []
    for card in cards:
        index = Rules().cards.index(card)
"""
        self.games = [[None, None],                     # no game
                      [0, 0], [2, 0], [3, 0],           # sauspiel
                      [None, 1],                        # wenz
                      [0, 2], [1, 2], [2, 2], [3, 2]]   # solo
                    # schelle # herz # gras # eichel

"""

def translate_cards_to_str(cards):
    cards_str = []
    for card in cards:
        if card[0] == 0:
            str = 'Schellen-'
        elif card[0] == 1:
            str = 'Herz-'
        elif card[0] == 2:
            str = 'Gras-'
        else:
            str = 'Eichel-'
        if card[1] == 0:
            str += '7'
        elif card[1] == 1:
            str += '8'
        elif card[1] == 2:
            str += '9'
        elif card[1] == 3:
            str += 'Unter'
        elif card[1] == 4:
            str += 'Ober'
        elif card[1] == 5:
            str += 'Koenig'
        elif card[1] == 6:
            str += '10'
        else:
            str += 'Ass'

        cards_str.append(str)
    return cards_str


def translate_games_to_str(game):
    if game == [None, None]:
        str = "Kein Spiel"
    elif game == [0, 0]:
        str = "auf die Schellen"
    elif game == [2, 0]:
        str = "auf die Gras"
    elif game == [3, 0]:
        str = "aus die Eichel"
    elif game == [None, 1]:
        str = "Wenz"
    elif game == [0, 2]:
        str = "Schellen-Solo"
    elif game == [1, 2]:
        str = "Herz-Solo"
    elif game == [2, 2]:
        str = "Gras-Solo"
    elif game == [3, 2]:
        str = "Eichel-Solo"
    return str