# opponent.py
import random


class Opponent:
    """
    Opponent to play against
    Lvl 1: Random moves
    """
    def __init__(self):
        pass

    def getMove(self, legal):
        """
        Chooses a random legal move to play
        :param legal: arr (list of legal moves in the current position)
        :return move: move object (computer's move, False if no legal moves found)
        """
        n = len(legal) - 1
        if n:
            return legal[random.randint(0, len(legal) - 1)]
        return False
