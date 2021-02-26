from Player import Player
from rules import Rules
import random


class RandomPlayer(Player):  #Player that chooses a game and cards randomly

    def __init__(self):
        super().__init__()

    def act(self, state):
        allowed_actions = state["allowed_actions"]
        if state["game_state"].game_stage == Rules.BIDDING:
            ## ToDo: Insert standard feed forward neural network - 2 layers a 50 neurons
            print("Random-Agent")
            print(state)
            breakpoint()
        selected_action = random.choice(allowed_actions)
        print("bidding round so far: %s", %s state['game_state'].bidding)
        return selected_action, 1
