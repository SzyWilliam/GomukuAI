from board_scorer import *
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
    def evaluate(board, x, y, move,trail=200,explore=4):
        """
        This function takes a board, evaluates the score (on behave of player 1)
        and returns the evaluated score

        :param board:  The current board (including the recent move)
        :param x:   last recent move's position x
        :param y:   last recent move's position y
        :param move: last recent move's player, move = 1 / 2
        :param trail:   number of simulations at each action
        :param explore: number of opponent's actions to be explored
        :return: a real value for the score of this recent move (the best winning rate among the following actions)
        """
        new_board = copy.deepcopy(board)
        new_board[x][y] = move # the player takes the current move 
        actions = MCTSScorer.findNeighbor(new_board,neighborNearBy=1)
        score = {}
        for action in actions:
            a_board = copy.deepcopy(new_board)
            a_board[action[0]][action[1]] = 3 - move
            score[action] = MCTSScorer.heuristic(a_board,action[0],action[1],3 - move)

        score = sorted(score.items(), key = lambda s:(s[1], s[0]))
        winrate = [0 for i in range(explore)]
        for i in range(explore):
            t = 0
            win = 0
            action = score[i][0]
            a_board = copy.deepcopy(new_board)
            a_board[action[0]][action[1]] = 3 - move
            while (t < trail):
                t += 1
                win += MCTSScorer.simulation(copy.deepcopy(a_board),move,player = move) 
            winrate[i] = win/t
            print(win)
        print(winrate)
        return min(winrate) # 返回最小胜率（minimax思想）

    @staticmethod
    def simulation(board,move,player):
        """
        To simulate a game randomly according to current board,
        :return: the winner
        """
        winner = MCTSScorer.judge(board)
        if winner != 0:
            # print(winner == move)
            return (winner == move)
        else:
            action = MCTSRandomMove.next_move(board,player)
            board[action[0]][action[1]] = player
            return MCTSScorer.simulation(board,move,3 - player)

    @staticmethod
    def judge(board):
        """
        To check if a final state is reached and the winner
        """
        patterDict = PatternExtractionScorer.patternCount(board)
        if patterDict['11111'][0] or patterDict['011110'][0]:
            # for i in board:print(i)
            return 1
        elif patterDict['11111'][1] or patterDict['011110'][1]:
            # for i in board:print(i)
            return 2
        return 0 

    @staticmethod
    def heuristic(board,x,y,move):
        """
        This function is used during the internal nodes pruning
        This method is used for better pruning strategy
        """
        return PatternExtractionScorer.evaluate(board,x,y,move)
    
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


if __name__ == "__main__":
    board = [[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    print(MCTSScorer.evaluate(board,0,1,1))