# from numpy import array
from itertools import product
# from scipy.signal import convolve2d
# import scipy

class Scorer:
    """
    This is the Scorer interface
    The responsibility of a Scorer:
    it takes a board and returns a value for that value
    """
    def evaluate(self, board):
        raise NotImplementedError("interface method should not be invoked")

# TODO Currently pattern
class PatternExtractionScorer(Scorer):
    @staticmethod
    def evaluate(board):
        return PatternExtractionScorer.score(board)

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
                       '0110': [0, 0],  # Add three new patterns for a quick start
                       '020': [0, 0],
                       '010': [0, 0],
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

        # # Count by row
        # for row in boardExtend1:
        #     line = ''.join(map(str, row))
        #     for pattern in patternDict.keys():
        #         patternDict[pattern][0] += line.count(pattern)
        # for row in boardExtend2:
        #     line = ''.join(map(str, row))
        #     for pattern in patternDict.keys():
        #         patternDict[pattern][1] += line.count(pattern)
        #
        # # Count by column
        # for col in list(array(boardExtend1).T):
        #     line = ''.join(map(str, col))
        #     for pattern in patternDict.keys():
        #         patternDict[pattern][0] += line.count(pattern)
        # for col in list(array(boardExtend2).T):
        #     line = ''.join(map(str, col))
        #     for pattern in patternDict.keys():
        #         patternDict[pattern][1] += line.count(pattern)

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
                     '0110': 2,
                     '020': 1,
                     '010': 1,
                     'double3': 20}
        patternDict = PatternExtractionScorer.patternCount(board)
        for pattern in patternDict.keys():
            score += (patternDict[pattern][0] - patternDict[pattern][1]) * scoreDict[pattern]
        return score


# class Conv2DScorer(Scorer):
#     def __init__(self):
#         self.convPatterns = []
#         self.convPatterns.append((np.array([
#             [1, 0, 0, 0, 0],
#             [0, 1, 0, 0, 0],
#             [0, 0, 1, 0, 0],
#             [0, 0, 0, 1, 0],
#             [0, 0, 0, 0, 1],
#         ]), (10000, 5)))
#
#         self.convPatterns.append((np.array([
#             [1, 0, 0, 0, 0],
#             [1, 0, 0, 0, 0],
#             [1, 0, 0, 0, 0],
#             [1, 0, 0, 0, 0],
#             [1, 0, 0, 0, 0],
#         ]), (10000, 5)))
#
#         self.convPatterns.append((np.array([
#             [0, 0, 0, 0, 1],
#             [0, 0, 0, 1, 0],
#             [0, 0, 1, 0, 0],
#             [0, 1, 0, 0, 0],
#             [1, 0, 0, 0, 0],
#         ]), (10000, 5)))
#
#         self.convPatterns.append((np.array([
#             [1, 1, 1, 1, 1],
#         ]), (10000, 5)))
#
#         self.convPatterns.append((np.array([
#             [1, 0, 0, 0],
#             [0, 1, 0, 0],
#             [0, 0, 1, 0],
#             [0, 0, 0, 1],
#         ]), (1000, 4)))
#         self.convPatterns.append((np.array([
#             [0, 0, 0, 1],
#             [0, 0, 1, 0],
#             [0, 1, 0, 0],
#             [1, 0, 0, 0],
#         ]), (1000, 4)))
#         self.convPatterns.append((np.array([
#             [1, 1, 1, 1],
#         ]), (1000, 4)))
#         self.convPatterns.append((np.array([
#             [1, 0, 0, 0],
#             [1, 0, 0, 0],
#             [1, 0, 0, 0],
#             [1, 0, 0, 0],
#         ]), (1000, 4)))
#
#         self.convPatterns.append((np.array([
#             [1, 0, 0],
#             [0, 1, 0],
#             [0, 0, 1],
#         ]), (500, 3)))
#         self.convPatterns.append((np.array([
#             [0, 0, 1],
#             [0, 1, 0],
#             [1, 0, 0],
#         ]), (500, 3)))
#         self.convPatterns.append((np.array([
#             [1, 0, 0],
#             [1, 0, 0],
#             [1, 0, 0],
#         ]), (500, 3)))
#         self.convPatterns.append((np.array([
#             [1, 1, 1],
#         ]), (500, 3)))
#
#         self.convPatterns.append((np.array([
#             [1, 0],
#             [0, 1],
#         ]), (50, 2)))
#
#         self.convPatterns.append((np.array([
#             [0, 1],
#             [1, 0],
#         ]), (50, 2)))
#
#         self.convPatterns.append((np.array([
#             [1, 0],
#             [1, 0],
#         ]), (50, 2)))
#
#         self.convPatterns.append((np.array([
#             [1, 1],
#         ]), (50, 2)))
#
#     def evaluate(self, rawBoard):
#         board = np.array(rawBoard)
#         board[board == 2] = -1
#
#         extentBoard = np.array(rawBoard)
#         extentBoard = 3 - extentBoard
#         extentBoard[extentBoard == 3] = 0
#         extentBoard[extentBoard == 2] = -1
#
#         value = 0
#         for (k, v) in self.convPatterns:
#             pattern = k
#             patternValue, patternActivateNum = v
#             value += Conv2DScorer.featureCount(board, pattern, patternActivateNum) * patternValue
#             value -= Conv2DScorer.featureCount(extentBoard, pattern, patternActivateNum) * patternValue
#         return value
#
#     @staticmethod
#     def featureCount(board, pattern, activateNum):
#         res = convolve2d(board, pattern, mode='valid')
#         res[res != activateNum] = 0
#         return scipy.count_nonzero(res)
#
#     @staticmethod
#     def conv2D(board, pattern, activateNum):
#         w, h = board.shape
#         w1, h1 = pattern.shape
#         board = np.pad(board, max(h1, w1), 'constant')
#
#         count = 0
#         for i in range(w):
#             for j in range(h):
#                 convSum = np.sum(board[i:i+w1, j:j+h1] * pattern)
#                 if convSum == activateNum:
#                     count += 1
#         return count
    
        


if __name__ == '__main__':
    board = np.array(
        [
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
        ]
    )

    pattern = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
