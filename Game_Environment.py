from collections import namedtuple

from Main import main

#_GameState = namedtuple("GameState", "names game_type turn teams order current_trick old_tricks points winner")

# Inheriting from a namedtuple is convenient because it makes the class
# immutable and predefines __init__, __repr__, __hash__, __eq__, and others
#class Gamestate(_GameState):
#    pass