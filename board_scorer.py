# from numpy import array
from itertools import product
# from scipy.signal import convolve2d
# import scipy
from copy import deepcopy
from brain import logDebug

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
        1000,  # live 3
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

    scoreDict = {'11111': live[5],  # win
                 '011110': live[4], # win
                 '011112': dead[4], # dead 4
                 '211110': dead[4], # dead 4
                 '01110': live[3],  # live 3
                 '01112': dead[3],  # dead 3
                 '21110': dead[3],  # dead 3
                 '0110': live[2],   # live 2
                 '2110': dead[2],   # dead 2
                 '0112': dead[2],   # dead 2
                 '010': live[1],    # live 1
                 '0111010': (live[5] / 3 + live[3]),  # live 3 ++
                 '0101110': (live[5] / 3 + live[3]),
                 '0110110': (live[5] / 3 + live[3]),

                 '2111010': (live[5] / 4 + dead[3]),  # dead 3++
                 '0111012': (live[5] / 4 + live[3]),
                 '2110110': (live[5] / 4 + live[2]),
                 '0110112': (live[5] / 4 + live[2]),
                 '2101110': (live[5] / 4 + live[3]),
                 '0101112': (live[5] / 4 + dead[3]),

                 '011010': (live[3] / 2 + live[2]),  # live 2 ++
                 '010110': (live[3] / 2 + live[2]),

                 '211010': (dead[4] / 2 + dead[2]),  # dead 2 ++
                 '011012': (dead[4] / 2 + dead[2]),
                 '210110': (dead[4] / 2 + dead[2]),
                 '010112': (dead[4] / 2 + dead[2]),
                 }

    compositeReward = 1.2

    @staticmethod
    def evaluate(board, x, y, move):
        return PatternExtractionScorer.score(board, 1) #+ PatternExtractionScorer.compositeScore(board, x, y, move)

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
        patternDict = {}
        for key in PatternExtractionScorer.scoreDict:
            patternDict[key] = [0, 0]

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
    def score(board, move):
        """
        Evaluate the score of player 1, according current board
        :returns an integer
        """
        score = 0
        scoreDict = PatternExtractionScorer.scoreDict
        patternDict = PatternExtractionScorer.patternCount(board)

        discount = 1.2
        for pattern in patternDict.keys():
            score += (patternDict[pattern][move-1] - discount * patternDict[pattern][2-move]) * scoreDict[pattern]
        return score

    @staticmethod
    def compositeScore(board, x, y, move):
        enemy_board = deepcopy(board)
        enemy_board[x][y] = 3-move
        my_live, my_dead = PatternExtractionScorer.compositePatternProposal(board, x, y, move)
        enemy_live, enemy_dead = PatternExtractionScorer.compositePatternProposal(enemy_board, x, y, 3-move)
        live = [my_live[i] + enemy_live[i] for i in range(len(my_live))]
        dead = [my_dead[i] + enemy_dead[i] for i in range(len(my_dead))]

        score = 0
        win = PatternExtractionScorer.live[5]
        live_score = PatternExtractionScorer.live
        dead_score = PatternExtractionScorer.dead
        if live[3] >= 2 or live[4] >= 1:  # double live 3 or live 4
            score = win
        elif live[3] >= 1 and dead[4] >= 1:  # live 3 + dead 4
            score = win
        elif live[3] >= 1 and live[4] >= 1:  # live 3 + live 4
            score = win
        elif dead[4] >= 2:  # double dead 4
            score = win
        elif sum(live[2:4]) + sum(dead[2:4]) >= 2:
            ret = 0
            for i in range(2, 5):
                ret += live[i] * live_score[i]
                ret += dead[i] * dead_score[i]
            score = PatternExtractionScorer.compositeReward * ret
        else:
            score = 0

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
        col_count += col_left + col_right

        col_live_side = col_left_live + col_right_live
        if col_live_side == 2:
            live[col_count] += 1
        elif col_live_side == 1:
            dead[col_count] += 1

        # row count
        row_right, row_right_live = PatternExtractionScorer._helperPatternCount(board, x, y, 0, +1, move, width, height)
        row_left, row_left_live = PatternExtractionScorer._helperPatternCount(board, x, y, 0, -1, move, width, height)
        row_count += row_right + row_left

        row_live_side = row_left_live + row_right_live
        if row_live_side == 2:
            live[row_count] += 1
        elif row_live_side == 1:
            dead[row_count] += 1

        # diag1 count
        diag1_left, diag1_left_live = PatternExtractionScorer._helperPatternCount(board, x, y, +1, +1, move, width, height)
        diag1_right, diag1_right_live = PatternExtractionScorer._helperPatternCount(board, x, y, -1, -1, move, width, height)
        diag1_count += diag1_left + diag1_right

        diag1_live_side = diag1_left_live + diag1_right_live
        if diag1_live_side == 2:
            live[diag1_count] += 1
        elif diag1_live_side == 1:
            dead[diag1_count] += 1

        # diag2 count
        diag2_left, diag2_left_live = PatternExtractionScorer._helperPatternCount(board, x, y, +1, -1, move, width, height)
        diag2_right, diag2_right_live = PatternExtractionScorer._helperPatternCount(board, x, y, -1, +1, move, width, height)
        diag2_count += diag2_left + diag2_right

        diag2_live_side = diag2_left_live + diag2_right_live
        if diag2_live_side == 2:
            live[diag2_count] += 1
        elif diag2_live_side == 1:
            dead[diag2_count] += 1

        return live, dead


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
            if not(0 <= x + x_index < width and 0 <= y + y_index < height):
                live_side = 0
                break
        return [count, live_side]



class FastScorer(Scorer):
    """
    This Scorer is designed for fast evaluation
    [000X000] [count, space, live_side]
    [2101110] [4 1 1]
    [2101010] [3 2 1]
    [1101101] [5 2 0]
    """
    live = [
        0,
        10,
        100,
        1000,
        4000,
        10000,
    ]

    sleep = [
        0,
        5,
        40,
        400,
        1500,
        8000,
    ]

    @staticmethod
    def evaluate(board, x, y, move):
        """
        This method should calculate the localized effects of the [x, y] move by player $move
        """
        score = FastScorer.score(board, x, y, move)
        logDebug("This method is called for [{},{}] and score is {}".format(x, y, score))
        return score

    @staticmethod
    def heuristic(board, x, y, move):
        return FastScorer.evaluate(board, x, y, move)

    @staticmethod
    def directionCountHelper(board, x, y, player, x_incr, y_incr, width, height):
        """
        This helper function calculates the one-direction connection
        ASSERT board[x][y] == player

        IF two more spaces in total founded: break immediately
        """
        x_index = x_incr
        y_index = y_incr
        player_count = 0
        space_count = 0
        is_live = True

        while 0 <= x + x_index < width and 0 <= y + y_index < height:
            if board[x + x_index][y + y_index] == player:
                player_count += 1
            else:
                if board[x + x_index][y + y_index] == 3 - player:
                    is_live = False
                    break
                else:
                    # can tolrate one space, under the condition of next place is 1
                    if (0 <= x + x_index + x_incr < width and 0 <= y + y_index + y_incr < height) and \
                      board[x + x_index + x_incr][y + y_index + y_incr] == player and \
                      space_count == 0:
                        space_count += 1
                    else:
                        break

            x_index += x_incr
            y_index += y_incr

            if not (0 <= x + x_index < width and 0 <= y + y_index < height):
                if board[x + x_index - x_incr][y + y_index - y_incr] == player:
                    is_live = False
                break

        return [player_count, space_count, is_live]

    @staticmethod
    def directionCountHelperSimple(board, x, y, x_incr, y_incr, move, width, height):
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
            if not (0 <= x + x_index < width and 0 <= y + y_index < height):
                live_side = 0
                break
        return [count, live_side]


    @staticmethod
    def directionCount(board, x, y, player, dir_x, dir_y, width, height):
        """
        :return: [category_number, category_live_or_sleep_or_dead]
        """
        # [p1, s1, l1] = FastScorer.directionCountHelper(board, x, y, player, dir_x, dir_y, width, height)
        # [p2, s2, l2] = FastScorer.directionCountHelper(board, x, y, player, -dir_x, -dir_y, width, height)
        #
        # live_side = 0
        # if l1: live_side += 1
        # if l2: live_side += 1

        # if s1 + s2 == 2:
            # adopt the simpler version
        [c1, ls1] = FastScorer.directionCountHelperSimple(board, x, y, player, dir_x, dir_y, width, height)
        [c2, ls2] = FastScorer.directionCountHelperSimple(board, x, y, player,-dir_x,-dir_y, width, height)
        return [c1 + c2 + 1, ls1 + ls2]

        # if live_side == 0:
        #     return [0, 0]
        #
        # # The most general case
        # return [p1 + p2 + 1 - s1 - s2, live_side]

    @staticmethod
    def pattern_num(board, x, y, player):
        live = [0] * 6
        sleep = [0] * 6
        pattern_count = [live, sleep]

        [col, col_live] = FastScorer.directionCount(board, x, y, player, 1, 0, len(board), len(board[0]))
        logDebug("col pattern [{},{}] is {} with state {}".format(x, y, col, col_live))
        if col_live != 0: pattern_count[2 - col_live][min(col, 5)] += 1

        [row, row_live] = FastScorer.directionCount(board, x, y, player, 0, 1, len(board), len(board[0]))
        logDebug("row pattern [{},{}] is {} with state {}".format(x, y, row, row_live))
        if row_live != 0: pattern_count[2 - row_live][min(row, 5)] += 1

        [diag1, diag1_live] = FastScorer.directionCount(board, x, y, player, 1, 1, len(board), len(board[0]))
        logDebug("diag1 pattern [{},{}] is {} with state {}".format(x, y, diag1, diag1_live))
        if diag1_live != 0: pattern_count[2 - diag1_live][min(diag1, 5)] += 1

        [diag2, diag2_live] = FastScorer.directionCount(board, x, y, player, 1, -1, len(board), len(board[0]))
        logDebug("diag2 pattern [{},{}] is {} with state {}".format(x, y, diag2, diag2_live))
        if diag2_live != 0: pattern_count[2 - diag2_live][min(diag2, 5)] += 1

        return pattern_count


    @staticmethod
    def score(board, x, y, player):
        enemy_board = deepcopy(board)
        enemy_board[x][y] = 3 - player
        [my_live, my_sleep] = FastScorer.pattern_num(board, x, y, player)
        [en_live, en_sleep] = FastScorer.pattern_num(enemy_board, x, y, 3 - player)

        final_score = 0
        r = 1.2
        for i in range(1, 6):
            final_score += my_live[i] * FastScorer.live[i]
            final_score += my_sleep[i] * FastScorer.sleep[i]

            final_score += r * en_live[i] * (FastScorer.live[i-1] - FastScorer.sleep[i-1])
            final_score += r * en_sleep[i] * FastScorer.sleep[i-1]

        if player == 1:
            return final_score
        else:
            return -final_score

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
            [0, 0, 2, 0, 1, 0, 0],
            [0, 0, 1, 2, 0, 1, 0],
            [0, 0, 1, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]]

    board1=[[1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0]]

    print(FastScorer.directionCount(board1, 3, 3, 1, 1, 1, len(board1), len(board1[1])))



