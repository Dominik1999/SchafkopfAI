import random

import numpy as np
import math
import pandas as pd

from utils import one_hot_encode_cards, translate_cards_to_str, translate_games_to_str, one_hot_encode_game, \
    one_hot_encode_position, one_hot_encode_protocol, one_hot_encode_game_chosen


def get_tensors_from_hd5_file(games_data):

    d = {'cards': [], 'position': [], 'protocol': [], 'label': [], 'points': []}
    df = pd.DataFrame(data=d)

    df.cards = [one_hot_encode_cards(cards) for cards in games_data.cards]
    df.position = [one_hot_encode_position(position) for position in games_data.position]
    df.protocol = [one_hot_encode_protocol(protocol) for protocol in games_data.protocol]
    df.label = [one_hot_encode_game_chosen(game) for game in games_data.label]
    df.points = [points for points in games_data.points]
    return df
