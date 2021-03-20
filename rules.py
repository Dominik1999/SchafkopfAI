import numpy as np
"""
This is mostly copied from https://github.com/tobiasemrich/SchafkopfRL/blob/master/schafkopfrl/rules.py
My initial approach, having the rules together with the Player Class worked, but not performant and it was
harder to use the Monte Carlo Tree Search.
"""


class Rules:

    # This class should contain all necessary rules for Get process_data to list at every state
    # the possible actions for the Player

    # phases of the game
    BIDDING = 1
    CONTRA = 2
    RETOUR = 3
    TRICK = 4

    # predefine trumps for every game for efficiency
    SAUSPIEL_TRUMPS = [[1, 0], [1, 1], [1, 2], [1, 5], [1, 6], [1, 7], [0, 3], [1, 3], [2, 3], [3, 3], [0, 4],
                       [1, 4], [2, 4], [3, 4]]
    SCHELLENSOLO_TRUMPS = [[0, 0], [0, 1], [0, 2], [0, 5], [0, 6], [0, 7], [0, 3], [1, 3], [2, 3], [3, 3], [0, 4],
                           [1, 4], [2, 4], [3, 4]]
    HERZSOLO_TRUMPS = [[1, 0], [1, 1], [1, 2], [1, 5], [1, 6], [1, 7], [0, 3], [1, 3], [2, 3], [3, 3], [0, 4],
                       [1, 4], [2, 4], [3, 4]]
    GRASSOLO_TRUMPS = [[2, 0], [2, 1], [2, 2], [2, 5], [2, 6], [2, 7], [0, 3], [1, 3], [2, 3], [3, 3], [0, 4],
                       [1, 4], [2, 4], [3, 4]]
    EICHELSOLO_TRUMPS = [[3, 0], [3, 1], [3, 2], [3, 5], [3, 6], [3, 7], [0, 3], [1, 3], [2, 3], [3, 3], [0, 4],
                         [1, 4], [2, 4], [3, 4]]
    WENZ_TRUMPS = [[0, 3], [1, 3], [2, 3], [3, 3]]

    def __init__(self):
        self.card_number = ['siebener',
                            'achter',
                            'neuner',
                            'unter',
                            'ober',
                            'koening',
                            'zehner',
                            'sau']
        self.card_color = ['schellen', 'herz', 'gras', 'eichel']

        self.card_scores = [0, 0, 0, 2, 3, 4, 10, 11]

        # schelle # herz # gras # eichel
        self.cards = [[0, 0], [1, 0], [2, 0], [3, 0],  # siebener
                      [0, 1], [1, 1], [2, 1], [3, 1],  # achter
                      [0, 2], [1, 2], [2, 2], [3, 2],  # neuner
                      [0, 3], [1, 3], [2, 3], [3, 3],  # unter
                      [0, 4], [1, 4], [2, 4], [3, 4],  # ober
                      [0, 5], [1, 5], [2, 5], [3, 5],  # koenig
                      [0, 6], [1, 6], [2, 6], [3, 6],  # zehner
                      [0, 7], [1, 7], [2, 7], [3, 7]]  # sau

        self.game_names = ['sauspiel', 'wenz', 'solo']

        self.games = [None, [None, None],               # unknown yet, no game
                      [0, 0], [2, 0], [3, 0],           # sauspiel
                      [None, 1],                        # wenz
                      [0, 2], [1, 2], [2, 2], [3, 2]]   # solo

        # no game, sauspiel, solo, wenz
        self.reward_basic = [0, 20, 50, 50]
        # normal, schneider, schneider-schwarz
        self.reward_schneider = [0, 10, 20]
        self.winning_thresholds = [0, 30, 60, 90, 119]

        self.reward_laufende = 10
        # normal, schneider, schneider-schwarz
        self.min_laufende = [3, 2, 3]

    def higher_card(self, game_type, card1, card2):
        # returns True if card2 is higher than card1

        sorted_trumps = self.get_sorted_trumps(game_type)
        if card1 not in sorted_trumps:
            if card2 not in sorted_trumps:
                if card2[0] != card1[0] or card2[1] < card1[1]:
                    return False
                else:
                    return True
            else:
                return True
        else:
            if card2 not in sorted_trumps:
                return False
            else:                                       # both cards are trumps
                if sorted_trumps.index(card1) < sorted_trumps.index(card2):
                    return True
                else:
                    return False

    def get_sorted_trumps(self, game_type):

        if game_type[1] == 0:                           # Sauspiel
            return self.SAUSPIEL_TRUMPS

        elif game_type[1] == 2:                         # Solo
            if game_type[0] == 0:
                return self.SCHELLENSOLO_TRUMPS
            elif game_type[0] == 1:
                return self.HERZSOLO_TRUMPS
            elif game_type[0] == 2:
                return self.GRASSOLO_TRUMPS
            elif game_type[0] == 3:
                return self.EICHELSOLO_TRUMPS

        else:                                              # Wenz
            return self.WENZ_TRUMPS

    def allowed_actions(self, game_state, player_cards):
        if game_state.game_stage == Rules.BIDDING:
            return self.allowed_games(player_cards)
        elif game_state.game_stage == Rules.CONTRA or game_state.game_stage == Rules.RETOUR:
            return self.allowed_contra_retour(game_state, player_cards)
        else:
            return self.allowed_cards(game_state, player_cards)

    def allowed_games(self, player_cards):
        """
        returns a list of allowed games, given the player hand. Generally, all games are allowed except
          - Sauspiel with color that player does not have
          - Sauspiel with color that player has the ace
        :param player_cards: list of player cards
        :type player_cards: list
        :return: list of allowed games
        :rtype: list
        """
        allowed_games = self.games.copy()
        allowed_games.pop(0)

        playable_colors = {color for [color, number] in player_cards if
                           number != 3 and  # unter
                           number != 4 and  # ober
                           color != 1 and  # herz
                           [color, 7] not in player_cards}  # not the ace
        for c in [0, 2, 3]:
            if c not in playable_colors:
                allowed_games.remove([c, 0])

        return allowed_games

    def allowed_cards(self, game_state, player_cards):
        """
        returns the cards that a player is allowed to play, given the player (specifically cards, position and davongelaufen)
        and the current game_state (specifically, first card of trick and game type)
        """
        allowed_cards = []

        trumps = self.get_sorted_trumps(game_state.game_type)
        rufsau = [game_state.game_type[0], 7]

        first_player_of_trick = game_state.first_player if game_state.trick_number == 0 else game_state.trick_owner[
            game_state.trick_number - 1]

        if game_state.current_player == first_player_of_trick:  # first player in this trick
            allowed_cards = player_cards.copy()

            # exception is the Rufsau color
            if (
                    game_state.game_type[1] == 0 and
                    rufsau in player_cards and not
                    game_state.current_player == game_state.davongelaufen
            ):
                ruf_sau_color_cards = [card for card in player_cards if
                                       (
                                               card[0] == game_state.game_type[0] and
                                               card not in trumps and
                                               card != rufsau
                                       )]
                if len(ruf_sau_color_cards) < 3:
                    for c in ruf_sau_color_cards:
                        allowed_cards.remove(c)
        else:                                                   # not first player in this trick must comply
            first_card = game_state.course_of_game_playerwise[game_state.trick_number][first_player_of_trick]
            if first_card in trumps:
                player_trumps = [card for card in player_cards if card in trumps]
                if len(player_trumps) > 0:
                    allowed_cards = player_trumps
                else:
                    allowed_cards = player_cards.copy()
            else:                                               # color of first card is not trump
                # if the player has the Suchsau and the color is played and
                # he has not davongelaufen then he has to play the ace
                if (
                        game_state.game_type[1] == 0 and
                        game_state.game_type[0] == first_card[0] and
                        rufsau in player_cards and not
                        game_state.current_player == game_state.davongelaufen
                ):
                    allowed_cards = [rufsau]

                else:
                    player_first_color_cards = [card for card in player_cards if
                                                card[0] == first_card[0] and card not in trumps]
                    if len(player_first_color_cards) > 0:
                        allowed_cards = player_first_color_cards
                    else:
                        allowed_cards = player_cards.copy()

            # remove rufsau if not gesucht and not davongelaufen and not last trick
            if (
                    game_state.game_type[1] == 0 and
                    rufsau in allowed_cards and not
                    (
                            first_card[0] == rufsau[0] or
                            game_state.current_player == game_state.davongelaufen or
                            game_state.trick_number == 7
                    )
            ):
                allowed_cards.remove(rufsau)

        return allowed_cards

    def allowed_contra_retour(self, game_state, player_cards):
        """
        returns if it is allowed for the player to double the game at the current point in the game
        :param game_state: current game state
        :return: [True, False]  if it is possible to double otherwise [False]
        """
        allowed = [False]

        if not np.any(game_state.contra) and game_state.game_stage == Rules.CONTRA:  # contra check
            allowed.append(True)
            # not allowed if you are the player or the team mate of the player
            if game_state.game_player == game_state.current_player or (
                    game_state.game_type[1] == 0 and
                    (
                            [game_state.game_type[0], 7] in player_cards)
            ):
                allowed = [False]
        elif np.any(game_state.contra) and not np.any(game_state.retour) and game_state.game_stage == Rules.RETOUR:  # retour check
            allowed = [False]
            # allowed if you are the player or the team mate of the player
            if game_state.game_player == game_state.current_player or (
                    game_state.game_type[1] == 0 and
                    [game_state.game_type[0], 7] in player_cards
            ):
                allowed.append(True)

        return allowed

    def highest_game(self, bidding_round, first_player):
        current_highest_game = [None, None]
        game_player = None
        for p in range(4):
            player_id = (first_player + p) % 4
            game_type = bidding_round[player_id]
            if current_highest_game[1] is None or (
                    not game_type[1] is None and
                    game_type[1] > current_highest_game[1]
            ):
                current_highest_game = game_type
                game_player = player_id
        return game_player, current_highest_game

    # return the player id who played the highest card in the trick, trick needs to be sorted by player id
    def trick_owner(self, trick, first_player, game_type):
        highest_card_index = first_player
        for i in range(1, 4):
            player_id = (first_player + i) % 4
            if self.higher_card(game_type, trick[highest_card_index], trick[player_id]):
                highest_card_index = player_id
        return highest_card_index

    # return the number of points in trick
    def count_points(self, trick_cards):
        return sum([self.card_scores[number] for color, number in trick_cards])
