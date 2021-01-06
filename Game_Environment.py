# Create dataclass with slots for faster creation time if needed later
# https://towardsdatascience.com/understand-how-to-use-namedtuple-and-dataclass-in-python-e82e535c3691


class Gamestate():
    def __init__(self, players):
        self.players = players      # players and their order
        self.current_turn = None    # who's turn it is
        self.teams = dict(          # which teams are known at that time
            ist_spieler=[],
            nicht_spieler=[]
        )
        self.points = dict(         # point distribution
            ist_spieler=0,
            nicht_spieler=0,
        )
        self.game_phase = None      # 1: def. game, 2: play tricks, 3: finalized, 4: terminated
        self.game_type = None       # normal or solo
        self.called_ace = None      # color of ace that is called
        self.played_tricks = {}     # already played tricks
        self.current_trick = {}     # what is the current trick
        self.winner = None          # who wins

    #def find_children(game_state):
        #if board.terminal:  # If the game is finished then no moves can be made
        #    return set()
        # Otherwise, you can make a move in each of the empty spots
        #return {
        #    board.make_move(i) for i, value in enumerate(board.tup) if value is None
        #}

    #def find_random_child(game_state):
        #if board.terminal:
        #    return None  # If the game is finished then no moves can be made
        #empty_spots = [i for i, value in enumerate(board.tup) if value is None]
        #return board.make_move(choice(empty_spots))

    #def reward(game_state):
        #if not board.terminal:
        #    raise RuntimeError(f"reward called on nonterminal board {board}")
        #if board.winner is board.turn:
        #    # It's your turn and you've already won. Should be impossible.
        #    raise RuntimeError(f"reward called on unreachable board {board}")
        #if board.turn is (not board.winner):
        #    return 0  # Your opponent has just won. Bad.
        #if board.winner is None:
        #    return 0.5  # Board is a tie
        # The winner is neither True, False, nor None
        #raise RuntimeError(f"board has unknown winner type {board.winner}")

    #def is_terminal(game_state):
        #return board.terminal

    #def make_move(game_state, index):
        #tup = board.tup[:index] + (board.turn,) + board.tup[index + 1 :]
        #turn = not board.turn
        #winner = _find_winner(tup)
        #is_terminal = (winner is not None) or not any(v is None for v in tup)
        #return TicTacToeBoard(tup, turn, winner, is_terminal)