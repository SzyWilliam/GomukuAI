# from numpy import array
from itertools import product
# from scipy.signal import convolve2d
# import scipy
#from brain import logDebug

class Scorer:
    """
    This is the Scorer interface
    The responsibility of a Scorer:
    it takes a board and returns a value for that value
    """
    @staticmethod
    def evaluate(board, x, y, move):
        raise NotImplementedError("interface method should not be invoked")

    @staticmethod
    def heuristic(board, x, y, move):
        raise NotImplementedError("interface method should not be invoked")

# TODO Currently pattern
class PatternExtractionScorer(Scorer):
    live = [
        0,    # live 0
        5,    # live 1
        50,   # live 2
        400,  # live 3
        4500, # live 4
        10000  # live 5
    ]
    dead = [
        0,    # dead 0
        1,    # dead 1
        15,   # dead 2
        150,  # dead 3
        700   # dead 4
    ]
    isFirstMove = False

    compositeReward = 1.5

    @staticmethod
    def evaluate(board, x, y, move):
        return PatternExtractionScorer.score(board) + PatternExtractionScorer.compositeScore(board, x, y, move)

    @staticmethod
    def heuristic(board, x, y, move):
        return PatternExtractionScorer.compositeScore(board, x, y, move)

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
                       '0110': [0, 0],
                       '2110': [0, 0],
                       '0112': [0, 0]
                        }

        # Extend the board by filling in the walls with 2;
        # Construct 2 extended boards for two players (save time for string match)
        width = len(board)
        height = len(board[0])
        boardExtend1 = [[0 for i in range(width + 2)] for j in range(height + 2)]
        boardExtend2 = [[0 for i in range(width + 2)] for j in range(height + 2)]
        for i, j in product(range(height), range(width)):
            if board[i][j] != 0: 
                boardExtend1[i+1][j+1] = board[i][j]
                boardExtend2[i+1][j+1] = 3 - board[i][j]

        for i in range(width + 2):
            boardExtend1[0][i],boardExtend1[width+1][i],boardExtend1[i][0],boardExtend1[i][width+1] = 2,2,2,2
            boardExtend2[0][i],boardExtend2[width+1][i],boardExtend2[i][0],boardExtend2[i][width+1] = 2,2,2,2

        # Count by row/column/diagonal-up/diagonal-down
        for i in range(width+2):
            row1 = boardExtend1[i]
            row2 = boardExtend2[i]
            col1 = [row[i] for row in boardExtend1]
            col2 = [row[i] for row in boardExtend2]
            diaup1 = [boardExtend1[x][i-x] for x in range(i)]
            diaup2 = [boardExtend2[x][i-x] for x in range(i)]
            diadn1 = [boardExtend1[x][x+width-i] for x in range(i+1)]
            diadn2 = [boardExtend2[x][x+width-i] for x in range(i+1)]
            
            row1 =  ''.join(map(str, row1))
            row2 =  ''.join(map(str, row2))
            col1 =  ''.join(map(str, col1))
            col2 =  ''.join(map(str, col2))
            diaup1 =  ''.join(map(str, diaup1))
            diaup2 =  ''.join(map(str, diaup2))
            diadn1 =  ''.join(map(str, diadn1))
            diadn2 =  ''.join(map(str, diadn2))

            for pattern in patternDict.keys():
                patternDict[pattern][0] += row1.count(pattern) + col1.count(pattern) + diaup1.count(pattern) + diadn1.count(pattern)
                patternDict[pattern][1] += row2.count(pattern) + col2.count(pattern) + diaup2.count(pattern) + diadn2.count(pattern)

        # patternDict['010'][0] /= 3
        # patternDict['010'][1] /= 3
        return patternDict

    @staticmethod
    def score(board):
        """
        Evaluate the score of player 1, according current board
        :returns an integer
        """
        score = 0
        scoreDict = {'11111': PatternExtractionScorer.live[5],  # win
                     '011110': PatternExtractionScorer.live[4],  # win
                     '011112': PatternExtractionScorer.dead[4],  # dead 4
                     '211110': PatternExtractionScorer.dead[4],
                     '0111010': (PatternExtractionScorer.live[3]/2 + PatternExtractionScorer.dead[3]),  # live 3 ++
                     '0101110': (PatternExtractionScorer.live[3]/2 + PatternExtractionScorer.dead[3]),
                     '0110110': (PatternExtractionScorer.live[3]/2 + PatternExtractionScorer.dead[3]),
                     '01110': PatternExtractionScorer.live[3],   # live 3
                     '01112': PatternExtractionScorer.dead[3],   # dead 3
                     '21110': PatternExtractionScorer.dead[3],
                     '011010': (PatternExtractionScorer.live[2]/2 + PatternExtractionScorer.dead[2]),  # live 2 ++
                     '010110': (PatternExtractionScorer.live[2]/2 + PatternExtractionScorer.dead[2]),
                     '0110': PatternExtractionScorer.live[2],    # live 2
                     '2110': PatternExtractionScorer.dead[2],   # dead 2
                     '0112': PatternExtractionScorer.dead[2],
                     '010':  PatternExtractionScorer.live[1]}
        patternDict = PatternExtractionScorer.patternCount(board)

        discount = 0
        if PatternExtractionScorer.isFirstMove:
            discount = 1.1
        else:
            discount = 0.9
        for pattern in patternDict.keys():
            #if sum(patternDict[pattern]) > 0:
                #logDebug("Pattern: {}, my: {}, enemy:{}".format(pattern, patternDict[pattern][0], patternDict[pattern][1]))
            score += (patternDict[pattern][0] - 1.1 * patternDict[pattern][1]) * scoreDict[pattern]
        return score

    @staticmethod
    def compositeScore(board, x, y, move):
        width = len(board)
        height = len(board[0])
        boardExtend2 = [[0 for i in range(width)] for j in range(height)]
        for i, j in product(range(len(board)), range(len(board))):
            if board[i][j] != 0:  # 改正了符号
                boardExtend2[i][j] = 3 - board[i][j]

        score = PatternExtractionScorer.compositePatternProposal(board, x, y, move) - \
                PatternExtractionScorer.compositePatternProposal(boardExtend2, x, y, 3-move)

        if move == 1:
            return score
        elif move == 2:
            return -score


    @staticmethod
    def compositePatternProposal(board, x, y, move):
        """
        This method takes a move place, and returns the value gained if this move is take
        :param board:
        :param x:
        :param y:
        :param move:
        :return:
        """
        width = len(board)
        height = len(board[0])

        live = [0] * 5
        dead = [0] * 5

        col_count = 1
        row_count = 1
        diag1_count = 1
        diag2_count = 1

        col_live_side = 2
        row_live_side = 2
        diag1_live_side = 2
        diag2_live_side = 2

        # col count
        col_right, col_right_live = PatternExtractionScorer._helperPatternCount(board, x, y, +1, 0, move, width, height)
        col_left, col_left_live = PatternExtractionScorer._helperPatternCount(board, x, y, -1, 0, move, height, width)
        col_count = col_left + col_right
        col_live_side = col_left_live + col_right_live
        if col_live_side == 2:
            live[col_count] += 1
        elif col_live_side == 1:
            dead[col_count] += 1

        # row count
        row_right, row_right_live = PatternExtractionScorer._helperPatternCount(board, x, y, 0, +1, move, width, height)
        row_left, row_left_live = PatternExtractionScorer._helperPatternCount(board, x, y, 0, -1, move, width, height)
        row_count = row_right + row_left
        row_live_side = row_left_live + row_right_live
        if row_live_side == 2:
            live[col_count] += 1
        elif row_live_side == 1:
            dead[col_count] += 1

        # diag1 count
        diag1_left, diag1_left_live = PatternExtractionScorer._helperPatternCount(board, x, y, +1, +1, move, width, height)
        diag1_right, diag1_right_live = PatternExtractionScorer._helperPatternCount(board, x, y, -1, -1, move, width, height)
        diag1_count = diag1_left + diag1_right
        diag1_live_side = diag1_left_live + diag1_right_live
        if diag1_live_side == 2:
            live[col_count] += 1
        elif diag1_live_side == 1:
            dead[col_count] += 1

        # diag2 count
        diag2_left, diag2_left_live = PatternExtractionScorer._helperPatternCount(board, x, y, +1, -1, move, width, height)
        diag2_right, diag2_right_live = PatternExtractionScorer._helperPatternCount(board, x, y, -1, +1, move, width, height)
        diag2_count = diag2_left + diag2_right
        diag2_live_side = diag2_left_live + diag2_right_live
        if diag2_live_side == 2:
            live[col_count] += 1
        elif diag2_live_side == 1:
            dead[col_count] += 1

        win = PatternExtractionScorer.live[5]
        live_score = PatternExtractionScorer.live
        dead_score = PatternExtractionScorer.dead
        if live[3] >= 2 or live[4] >= 1:     # double live 3 or live 4
            return win
        elif live[3] >= 1 and dead[4] >= 1:  # live 3 + dead 4
            return win
        elif live[3] >= 1 and live[4] >= 1:  # live 3 + live 4
            return win
        elif dead[4] >= 2:                   # double dead 4
            return win
        elif sum(live[2:4]) + sum(dead[2:4]) >= 2:
            ret = 0
            for i in range(2, 5):
                ret += live[i] * live_score[i]
                ret += dead[i] * dead_score[i]
            return PatternExtractionScorer.compositeReward * ret
        else:
            return 0


    @staticmethod
    def _helperPatternCount(board, x, y, x_incr, y_incr, move, width, height):
        x_index = x_incr
        y_index = y_incr
        count = 0
        live_side = 1
        while 0 <= x + x_index < width and 0 <= y + y_index < height:
            if board[x + x_index][y + y_index] == move:
                count += 1
            else:
                if board[x + x_index][y + y_index] == 3 - move:
                    live_side -= 1
                break
            x_index += x_incr
            y_index += y_incr
        return [count, live_side]




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
    board =[[2, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 1, 0, 1, 0],
            [0, 0, 1, 0, 2, 0, 0],
            [0, 0, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 1]]

    PatternExtractionScorer.compositePatternProposal(board, 2, 2, 1)

