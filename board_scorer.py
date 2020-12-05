import numpy as np
from itertools import product

class Scorer:
    """
    This is the Scorer interface
    The responsibility of a Scorer:
    it takes a board and returns a value for that value
    """
    @staticmethod
    def evaluate(board):
        raise NotImplementedError("interface method should not be invoked")


class PatternExtractionScorer(Scorer):
    @staticmethod
    def evaluate(board):
        return 0

    @staticmethod
    def patternCount(board):
        """
        Count the stone patterns on board.
        Define the patterns:
            FIVE: 5 stones in a line 							 				*****
            FOURa: 4 stones in a line with both ends open  						 ****
            FOURb: 4 stones in a line with only 1 end open  					`****
            FOURc: 4 stones cut apart by one open cell with both ends open     ** **/* ***
            THREEa: 3 stones in a line with both ends open  					 ***
            THREEb: 3 stones in a line with only 1 end open 					`***
            THREEc: 3 stones cut apart by one open cell with both ends open      * **
            THREE2: 2 * 3 stones across with both ends open                      shuangsan
            TWOa: 2 stones in a line with both ends open 						 **
        :returns a dict: {patternstr:(player1_count,player2_count)}
        """
        patternDict = {'11111': [0, 0],
                       '011110': [0, 0],
                       '011112': [0, 0],
                       '211110': [0, 0],
                       '0111010': [0, 0],
                       '0101110': [0, 0],
                       '0110110': [0, 0],
                       '01110': [0, 0],
                       '01112': [0, 0],
                       '21110': [0, 0],
                       '011010': [0, 0],
                       '010110': [0, 0],
                       '0220': [0, 0],
                       'double3': [0, 0]}

        # Extend the board by filling in the walls with 0;
        # Construct 2 extended boards for two players (save time for string match)
        width = len(board)
        height = len(board[0])
        boardExtend1 = [[0 for i in range(width + 1)] for j in range(height + 1)]
        boardExtend2 = [[0 for i in range(width + 1)] for j in range(height + 1)]
        for i, j in product(range(len(board)), range(len(board))):
            if board[i][j] != 1:
                boardExtend1[i][j] = board[i][j]
                boardExtend2[i][j] = 3 - board[i][j]

        # Count by row
        for row in boardExtend1:
            line = ''.join(map(str, row))
            for pattern in patternDict.keys():
                patternDict[pattern][0] += line.count(pattern)
        for row in boardExtend2:
            line = ''.join(map(str, row))
            for pattern in patternDict.keys():
                patternDict[pattern][1] += line.count(pattern)

        # Count by column
        for col in list(np.array(boardExtend1).T):
            line = ''.join(map(str, col))
            for pattern in patternDict.keys():
                patternDict[pattern][0] += line.count(pattern)
        for col in list(np.array(boardExtend2).T):
            line = ''.join(map(str, col))
            for pattern in patternDict.keys():
                patternDict[pattern][1] += line.count(pattern)

        # Count by diagonal
        for i in range(len(boardExtend1)):
            line = ''
            for j in range(1 - i):
                line = line + str(boardExtend1[i][j])
            for pattern in patternDict.keys():
                patternDict[pattern][0] += line.count(pattern)
        for i in range(len(boardExtend2)):
            line = ''
            for j in range(1 - i):
                line = line + str(boardExtend2[i][j])
            for pattern in patternDict.keys():
                patternDict[pattern][1] += line.count(pattern)

        # Count double3
        # TODO double 3
        # 待补

        return patternDict

    @staticmethod
    def score(board):
        """
        Evaluate the score of player 1, according current board
        :returns an integer
        """
        score = 0
        scoreDict = {'11111': 5000,
                     '011110': 5000,
                     '011112': 10,
                     '211110': 10,
                     '0111010': 12,
                     '0101110': 12,
                     '0110110': 12,
                     '01110': 8,
                     '01112': 6,
                     '21110': 6,
                     '011010': 4,
                     '010110': 4,
                     '0220': 2,
                     'double3': 20}
        patternDict = PatternExtractionScorer.patternCount(board)
        for pattern in patternDict.keys():
            score += (patternDict[pattern][0] - patternDict[pattern][1]) * scoreDict[pattern]
        return score