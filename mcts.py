from board_scorer import Scorer,PatternExtractionScorer
import random
from itertools import product
import copy 

class MCTSMovePicker:
    @staticmethod
    def next_move(board, player):
        raise NotImplementedError("interface method should not be invoked")


class MCTSRandomMove(MCTSMovePicker):
    @staticmethod
    def next_move(board, player):
        actions = MCTSScorer.findNeighbor(board,neighborNearBy=1)
        return random.choice(actions)
        # raise NotImplementedError("Implement me")


class MCTSScorer(Scorer):
    """
    Scorer that is based on the MCTS method
    """
    @staticmethod
    def evaluate(board, x, y, move,trail=500):
        """
        This function takes a board, evaluates the score (on behave of player 1)
        and returns the evaluated score

        :param board:  The current board (including the recent move)
        :param x:   last recent move's position x
        :param y:   last recent move's position y
        :param move: last recent move's player, move = 1 / 2
        :param trail:   number of simulations at each action
        :return: a real value for the score of this recent move (the best winning rate among the following actions)
        """
        new_board = copy.deepcopy(board)
        new_board[x][y] = move # the player takes the current move 
        t = 0
        win = 0
        while (t < trail):
            t += 1
            win += MCTSScorer.simulation(new_board,move,player = 3 - move) # simulate winner 
        return (win/t)
        # raise NotImplementedError("Implement it")

    @staticmethod
    def simulation(board,move,player):
        """
        To simulate a game randomly according to current board,
        :return: the winner
        """
        winner = MCTSScorer.judge(board,move)
        if winner == move:
            return 1
        elif winner == 3 - move:
            return 0
        else:
            board[MCTSRandomMove.next_move(board,player)] = player
            return MCTSScorer.simulation(board,move,3 - player)

    @staticmethod
    def judge(board, move):
        """
        To check if a final state is reached
        """
        patterDict = PatternExtractionScorer.patternCount(board)
        if patterDict['11111'][move - 1] or patterDict['011110'][move - 1]:
            return move
        elif patterDict['11111'][2 - move] or patterDict['011110'][2 - move]:
            return 3 - move
        return 0 

    @staticmethod
    def heuristic(board, move):
        """
        This function is used during the internal nodes pruning
        This method is used for better pruning strategy
        TODO is it really needed for MCTS?
        """
        return 0
    
    @staticmethod
    def findNeighbor(board, neighborNearBy=1):
        """
        Find all open positions 1 cell away
        TODO Enable more general neighbor discovering strategy
        :param board:
        :param neighborNearBy: how much distance
        :return: a list of binary tuples.
        """
        neighbors = []
        stones = [(i, j) for i in range(len(board)) for j in range(len(board)) if board[i][j] != 0]
        for stone in stones:
            for i, j in product(range(stone[0] - 1, stone[0] + 2), range(stone[1] - 1, stone[1] + 2)):
                if (i, j) in product(range(len(board)), range(len(board))) and (i, j) not in neighbors and (
                        i, j) not in stones:
                    neighbors.append((i, j))
        return neighbors

