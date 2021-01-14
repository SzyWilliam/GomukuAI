'''
Basic Functions
'''
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG
from minimax import *
from board_scorer import *

pp.infotext = 'name="pbrain-minmax", version="1.0"'

MAX_BOARD = 20
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]

<<<<<<< HEAD
DEBUG_LOGFILE = "E:/FOR COURSES/大三/人工智能/PJ/pj final/pbrain-minmax/GomukuAI/log.txt"
=======
# DEBUG_LOGFILE = "D:/Gomuku AI/FinalPJ/GomukuAI/dist/log.txt"
>>>>>>> a220564461401ac553f3426a5e553bc7179b8e2f

# # ...and clear it initially
# with open(DEBUG_LOGFILE, "w") as f:
#     pass


# # define a function for writing messages to the file
# def logDebug(msg):
#     with open(DEBUG_LOGFILE, "a") as f:
#         f.write(msg + "\n")
#         f.flush()


# # define a function to get exception traceback
# def logTraceBack():
#     import traceback
#     with open(DEBUG_LOGFILE, "a") as f:
#         traceback.print_exc(file=f)
#         f.flush()
#     raise


def brain_init():
    if pp.width < 5 or pp.height < 5:
        pp.pipeOut("ERROR size of the board")
        return
    if pp.width > MAX_BOARD or pp.height > MAX_BOARD:
        pp.pipeOut("ERROR Maximal board size is {}".format(MAX_BOARD))
        return
    pp.pipeOut("OK")


def brain_restart():
    for x in range(pp.width):
        for y in range(pp.height):
            board[x][y] = 0
    pp.pipeOut("OK")


def isFree(x, y):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0


def brain_my(x, y):
    if isFree(x, y):
        board[x][y] = 1
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))


def brain_opponents(x, y):
    if isFree(x, y):
        board[x][y] = 2
    else:
        pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))


def brain_block(x, y):
    if isFree(x, y):
        board[x][y] = 3
    else:
        pp.pipeOut("ERROR winning move [{},{}]".format(x, y))


def brain_takeback(x, y):
    if x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] != 0:
        board[x][y] = 0
        return 0
    return 2


def brain_turn():
    global board


    if pp.terminateAI:
        return

<<<<<<< HEAD
=======
    # try:
>>>>>>> a220564461401ac553f3426a5e553bc7179b8e2f
    # Openning: play at the middle
    if sum(map(sum, board)) == 0:
        pp.do_mymove(int(len(board)/2), int(len(board)/2))
    else:
        # logDebug("Calling brain turn")

        minmaxTree = GomukuMinmaxTree(
            initialBoard=board,
            player=1,
            scorer=PatternExtractionScorer(),
            nodePosition=None,
            maxDepth=4,
            currentDepth=0
        )
        _, nextPosition = minmaxTree.solveMinmaxWithABPruning()
        pp.do_mymove(nextPosition[0], nextPosition[1])
<<<<<<< HEAD

=======
    # except:
    #     logTraceBack()
>>>>>>> a220564461401ac553f3426a5e553bc7179b8e2f


def brain_end():
    pass


def brain_about():
    pp.pipeOut(pp.infotext)


# "overwrites" functions in pisqpipe module
pp.brain_init = brain_init
pp.brain_restart = brain_restart
pp.brain_my = brain_my
pp.brain_opponents = brain_opponents
pp.brain_block = brain_block
pp.brain_takeback = brain_takeback
pp.brain_turn = brain_turn
pp.brain_end = brain_end
pp.brain_about = brain_about
# if DEBUG_EVAL:
#     pp.brain_eval = brain_eval


def main():
    pp.main()


if __name__ == "__main__":
    main()
