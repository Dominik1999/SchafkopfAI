import tensorflow as tf
import numpy as np
import random

import rules
from utils import one_hot_encode_cards, translate_cards_to_str, one_hot_encode_position, one_hot_encode_protocol

model = tf.keras.models.load_model('/home/pirate/PycharmProjects/SchafkopfAI/models/trained_models/bidding-pos-nn')
hands = []
position = 0
protocol = [None, None, None, None]

for i in range(100):
      hand = [hand for hand in random.sample(rules.Rules().cards, 8)]
      hands.append(hand)

for hand in hands:
      prediction = model.predict(x={'x1': np.array([one_hot_encode_cards(hand)]), 'x2': np.array([one_hot_encode_position(position)]), 'x3': np.array([one_hot_encode_protocol(protocol)])})
      choice = np.argsort(np.max(prediction, axis=0))[-1]
      if choice == 0 and 0.5 < np.amax(prediction) < 0.85:
            second_choice = np.argsort(np.max(prediction, axis=0))[-2]
            print(f"Cards: {translate_cards_to_str(hand)}, Position: {position},\n"
                  f"First Choice: {rules.Rules().games[choice + 1]}),\n"
                  f"Second Choice: {rules.Rules().games[second_choice + 1]}, \n"
                  f"Predictions: {prediction}")

"""
        self.games = [[None, None],                     # no game
                      [0, 0], [2, 0], [3, 0],           # sauspiel
                      [None, 1],                        # wenz
                      [0, 2], [1, 2], [2, 2], [3, 2]]   # solo
                    # schelle # herz # gras # eichel

        self.cards = [[0, 0], [1, 0], [2, 0], [3, 0],  # siebener
              [0, 1], [1, 1], [2, 1], [3, 1],  # achter
              [0, 2], [1, 2], [2, 2], [3, 2],  # neuner
              [0, 3], [1, 3], [2, 3], [3, 3],  # unter
              [0, 4], [1, 4], [2, 4], [3, 4],  # ober
              [0, 5], [1, 5], [2, 5], [3, 5],  # koenig
              [0, 6], [1, 6], [2, 6], [3, 6],  # zehner
              [0, 7], [1, 7], [2, 7], [3, 7]]  # sau
"""