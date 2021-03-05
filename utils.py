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


def one_hot_encode_position(position):
    one_hot_position = np.zeros(4)
    one_hot_position[position] = 1
    return one_hot_position


def one_hot_games(games):
    one_hot_games = np.zeros(9)
    for game in games:
        one_hot_games[Rules().games.index(game)] = 1
    return one_hot_games


def one_hot_encode_card(card):
    single_one_hot_card = np.zeros(32)
    single_one_hot_card[Rules().cards.index(card)] = 1
    return single_one_hot_card


def one_hot_encode_cards(cards, game_type=None):
    hand = sort_hand(cards, game_type)
    enc_cards = np.zeros((8, 32))
    for card, i in zip(hand, range(8)):
        enc_cards[i] = one_hot_encode_card(card)
    return enc_cards


def one_hot_encode_result(result):
    enc_result = np.zeros(2)
    enc_result[result] = 1
    return enc_result


def sort_hand(cards, game_type):
    if not game_type:
        return sorted(cards, key=lambda card: Rules().cards.index(card))

    sorted_trumps = Rules().get_sorted_trumps(game_type=game_type)
    trumps = sorted([card for card in cards if card in sorted_trumps], key= lambda card : sorted_trumps.index(card))
    non_trumps = sorted([card for card in cards if card not in sorted_trumps], key=lambda card: Rules().cards.index(card))

    return non_trumps + trumps


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
            card_str = 'Schellen-'
        elif card[0] == 1:
            card_str = 'Herz-'
        elif card[0] == 2:
            card_str = 'Gras-'
        else:
            card_str = 'Eichel-'
        if card[1] == 0:
            card_str += '7'
        elif card[1] == 1:
            card_str += '8'
        elif card[1] == 2:
            card_str += '9'
        elif card[1] == 3:
            card_str += 'Unter'
        elif card[1] == 4:
            card_str += 'Ober'
        elif card[1] == 5:
            card_str += 'Koenig'
        elif card[1] == 6:
            card_str += '10'
        else:
            card_str += 'Ass'

        cards_str.append(card_str)
    return cards_str


def translate_games_to_str(game):
    if game == [None, None]:
        card_str = "Kein Spiel"
    elif game == [0, 0]:
        card_str = "auf die Schellen"
    elif game == [2, 0]:
        card_str = "auf die Gras"
    elif game == [3, 0]:
        card_str = "aus die Eichel"
    elif game == [None, 1]:
        card_str = "Wenz"
    elif game == [0, 2]:
        card_str = "Schellen-Solo"
    elif game == [1, 2]:
        card_str = "Herz-Solo"
    elif game == [2, 2]:
        card_str = "Gras-Solo"
    elif game == [3, 2]:
        card_str = "Eichel-Solo"
    return card_str