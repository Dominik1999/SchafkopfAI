import rules
from monte_carlo_tree_search.mct import MonteCarloTree
from game_state import PublicGameState
from rules import Rules
from game_environment import SchafkopfEnv
from agents.Player import Player
import random
import tensorflow as tf
import numpy as np

from utils import one_hot_encode_cards, one_hot_encode_position, one_hot_encode_protocol


class BNNPIMCPlayer(Player):

    def __init__(self, samples, playouts, agent):
        super().__init__()
        self.samples = samples
        self.playouts = playouts
        self.agent = agent
        self.bidding_nn = tf.keras.models.load_model('/home/pirate/PycharmProjects/SchafkopfAI/models/trained_models/bidding-pos-nn')

    def act(self, state):
        if state["game_state"].game_stage == Rules.BIDDING:
            return self.bidding(state["game_state"], state["current_player_cards"])
        else:
            return self.run_mcts(state["game_state"], state["current_player_cards"])

    def bidding(self, game_state, player_cards):
        hand = player_cards
        protocol = (
                game_state.bidding_round[game_state.first_player:] +
                game_state.bidding_round[:game_state.first_player])
        position = game_state.current_player - game_state.first_player
        probabilities = self.bidding_nn.predict(
            x={
                'x1': np.array([one_hot_encode_cards(hand)]),
                'x2': np.array([one_hot_encode_position(position)]),
                'x3': np.array([one_hot_encode_protocol(protocol)])})

        choice = np.argsort(np.max(probabilities, axis=0))[-1]
        if choice == 0 and 0.5 < np.amax(probabilities) < 0.85:         # Bidding NN is really biased and shout play way more aggressive
            choice = np.argsort(np.max(probabilities, axis=0))[-2]

        game_to_choose = self.rules.games[choice + 1]
        allowed_actions = self.rules.allowed_actions(game_state, player_cards)

        if game_to_choose not in allowed_actions:
            while game_to_choose not in allowed_actions:
                probabilities.pop(np.argmax(probabilities))
                game_to_choose = self.rules.games[np.argmax(probabilities) + 1]

        return game_to_choose, np.amax(probabilities)

    def run_mcts(self, game_state, player_cards):
        cummulative_action_count_rewards = {}

        for i in range(self.samples):
            sampled_player_hands = self.sample_player_hands(game_state, player_cards)
            mct = MonteCarloTree(game_state, sampled_player_hands, self.rules.allowed_actions(game_state, player_cards),
                                 player=self.agent)
            mct.uct_search(self.playouts)
            action_count_rewards = mct.get_action_count_rewards()

            for action in action_count_rewards:
                if action in cummulative_action_count_rewards:
                    cummulative_action_count_rewards[action] = (
                        cummulative_action_count_rewards[action][0] + action_count_rewards[action][0],
                        [cummulative_action_count_rewards[action][1][i] + action_count_rewards[action][1][i] for i in
                         range(4)])
                else:
                    cummulative_action_count_rewards[action] = action_count_rewards[action]

        best_action = max(cummulative_action_count_rewards.items(), key=lambda x: x[1][0])[0]
        visits = cummulative_action_count_rewards[best_action][0]
        if isinstance(best_action, tuple):
            best_action = list(best_action)
        return best_action, visits / sum([x[0] for x in cummulative_action_count_rewards.values()])

    def sample_player_hands(self, game_state, ego_player_hand):

        # precomputations
        played_cards = [card for trick in game_state.course_of_game for card in trick if card != [None, None]]
        remaining_cards = [card for card in self.rules.cards if
                           ((card not in played_cards) and (card not in ego_player_hand))]

        needed_player_cards = [8, 8, 8, 8]

        for trick in range(game_state.trick_number + 1):
            for i, card in enumerate(game_state.course_of_game_playerwise[trick]):
                if card != [None, None]:
                    needed_player_cards[i] -= 1

        needed_player_cards[game_state.current_player] = 0

        valid_card_distribution = False
        player_cards = None

        # loop over random card distributions until we found a valid one
        while not valid_card_distribution:

            # randomly distribute cards so that each player gets as many as he needs
            valid_card_distribution = True
            player_cards = [[], [], [], []]
            player_cards[game_state.current_player] = ego_player_hand
            random.shuffle(remaining_cards)

            from_card = 0
            for i, nededed_cards in enumerate(needed_player_cards):
                if i == game_state.current_player:
                    continue
                player_cards[i] = remaining_cards[from_card:from_card + nededed_cards]
                from_card += nededed_cards

            # check if with the current card distribution every made move was valid
            schafkopf_env = SchafkopfEnv()
            state, _, _ = schafkopf_env.set_state(PublicGameState(game_state.dealer), player_cards)

            while True:
                eval_game_state, allowed_actions = state["game_state"], state["allowed_actions"]

                if eval_game_state.game_stage == Rules.BIDDING:
                    action = eval_game_state.bidding_round[eval_game_state.current_player]
                    if action == None:
                        break
                    elif action not in allowed_actions:
                        valid_card_distribution = False
                        break
                elif eval_game_state.game_stage == Rules.CONTRA:
                    action = eval_game_state.contra[eval_game_state.current_player]
                    if action == None:
                        break
                    elif action not in allowed_actions:
                        valid_card_distribution = False
                        break
                elif eval_game_state.game_stage == Rules.RETOUR:
                    action = eval_game_state.retour[eval_game_state.current_player]
                    if action == None:
                        break
                    elif action not in allowed_actions:
                        valid_card_distribution = False
                        break
                else:
                    action = eval_game_state.course_of_game_playerwise[eval_game_state.trick_number][
                        eval_game_state.current_player]
                    if action == [None, None]:
                        break
                    elif action not in allowed_actions:
                        valid_card_distribution = False
                        break
                state, _, _ = schafkopf_env.step(action)

        return player_cards
