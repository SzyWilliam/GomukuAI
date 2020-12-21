from board_scorer import Scorer
import random


class MCTSMovePicker:
    @staticmethod
    def next_move(board, player):
        raise NotImplementedError("interface method should not be invoked")


class MCTSRandomMove(MCTSMovePicker):
    @staticmethod
    def next_move(board, player):
        raise NotImplementedError("Implement me")


class MCTSScorer(Scorer):
    """
    Scorer that is based on the MCTS method
    """
    @staticmethod
    def evaluate(board, x, y, move):
        """
        This function takes a board, evaluates the score (on behave of player 1)
        and returns the evaluated score

        :param board:  The current board (including the recent move)
        :param x:   last recent move's position x
        :param y:   last recent move's position y
        :param move: last recent move's player, move = 1 / 2
        :return: a real value for the score of this recent move
        """
        raise NotImplementedError("Implement it")

    @staticmethod
    def heuristic(board, x, y, move):
        """
        This function is used during the internal nodes pruning
        This method is used for better pruning strategy
        TODO is it really needed for MCTS?
        """
        return 0
