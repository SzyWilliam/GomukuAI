'''
Basic Functions
'''

import random
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG
from itertools import product
import numpy as np
import copy

pp.infotext = 'name="pbrain-minmax", version="1.0"'

MAX_BOARD = 100
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]

DEBUG_LOGFILE = "E:/FOR COURSES/大三/人工智能/PJ/pj final/pbrain-minmax/pbrain-minmax.log"

# ...and clear it initially
with open(DEBUG_LOGFILE, "w") as f:
	pass


# define a function for writing messages to the file
def logDebug(msg):
	with open(DEBUG_LOGFILE,"a") as f:
		f.write(msg+"\n")
		f.flush()


# define a function to get exception traceback
def logTraceBack():
	import traceback
	with open(DEBUG_LOGFILE,"a") as f:
		traceback.print_exc(file=f)
		f.flush()
	raise 

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
	if isFree(x,y):
		board[x][y] = 1
	else:
		pp.pipeOut("ERROR my move [{},{}]".format(x, y))

def brain_opponents(x, y):
	if isFree(x,y):
		board[x][y] = 2
	else:
		pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))

def brain_block(x, y):
	if isFree(x,y):
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
	try:
		# 待改
		if pp.terminateAI:
			return

		logDebug("Calling brain turn")
		root = constructTree(board, player=1, nodePosition=None)
		logDebug("Constructed a Minmax Tree")
		val = value(root, -float('inf'), float('inf'))
		logDebug("Calculated a Minmax Value")
		nextPosition = None
		for succ in root.successor:
			if succ.value == val:
				nextPosition = succ.position

		pp.do_mymove(nextPosition[0], nextPosition[1])
	except:
		logTraceBack()


def brain_end():
	pass

def brain_about():
	pp.pipeOut(pp.infotext)

def getStones(board,player):
	"""
	Find all stones of the given player
	:returns a list of binary tuples.
	"""   	
	stones = [(i,j) for i in range(len(board)) for j in range(len(board)) if board[i][j]==player]
	return stones

def findNeighbor(board):
	"""
	Find all open positions less than 3 cells away
	:returns a list of binary tuples.
	"""
	neighbors = []
	stones = getStones(board,1) + getStones(board,2)
	for stone in stones:
		for i,j in product(range(stone[0]-1,stone[0]+2),range(stone[1]-1,stone[1]+2)):
			if (i,j) in product(range(len(board)),range(len(board))) and (i,j) not in neighbors and (i,j) not in stones:
					neighbors.append((i,j))
	return neighbors

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
	patternDict = {'11111':(0,0),
				 '011110':(0,0),
				 '011112':(0,0),
				 '211110':(0,0),
				 '0111010':(0,0),
				 '0101110':(0,0),
				 '0110110':(0,0),
				 '01110':(0,0),
				 '01112':(0,0),
				 '21110':(0,0),
				 '011010':(0,0),
				 '010110':(0,0),
				 '0220':(0,0),
				 'double3':(0,0)}

	# Extend the board by filling in the walls with 0;
	# Construct 2 extended boards for two players (save time for string match)
	boardExtend1 = [[0 for i in range(MAX_BOARD+1)] for j in range(MAX_BOARD+1)]
	boardExtend2 = [[0 for i in range(MAX_BOARD+1)] for j in range(MAX_BOARD+1)]
	for i,j in product(range(len(board)),range(len(board))) :
		if board[i][j] != 1:
			boardExtend1[i][j] = board[i][j]
			boardExtend2[i][j] = 3 - board[i][j]
	
	# Count by row
	for row in boardExtend1:
		line = ''.join(map(str,row))
		for pattern in patternDict.keys():
			patternDict[pattern][0] += line.count(pattern)
	for row in boardExtend2:
		line = ''.join(map(str,row))
		for pattern in patternDict.keys():
			patternDict[pattern][1] += line.count(pattern)
			
	# Count by column
	for col in list(np.array(boardExtend1).T):
		line = ''.join(map(str,col))
		for pattern in patternDict.keys():
			patternDict[pattern][0] += line.count(pattern)
	for col in list(np.array(boardExtend2).T):
		line = ''.join(map(str,col))
		for pattern in patternDict.keys():
			patternDict[pattern][1] += line.count(pattern)
		
	# Count by diagonal
	for i in range(len(boardExtend1)):
		line = ''
		for j in range(1-i):
			line = line + str(boardExtend1[i][j])
		for pattern in patternDict.keys():
			patternDict[pattern][0] += line.count(pattern)
	for i in range(len(boardExtend2)):
		line = ''
		for j in range(1-i):
			line = line + str(boardExtend2[i][j])
		for pattern in patternDict.keys():
			patternDict[pattern][1] += line.count(pattern)

	# Count double3
	# 待补

	return patternDict


def score(board):
	"""
	Evaluate the score of player 1, according current board
	:returns an integer
	"""	  
	score = 0
	scoreDict = {'11111':5000,
				 '011110':5000,
				 '011112':10,
				 '211110':10,
				 '0111010':12,
				 '0101110':12,
				 '0110110':12,
				 '01110':8,
				 '01112':6,
				 '21110':6,
				 '011010':4,
				 '010110':4,
				 '0220':2,
				 'double3':20}
	patternDict = patternCount(board)
	for pattern in patternDict.keys():
		score += (patternDict[pattern][0]-patternDict[pattern][1]) * scoreDict[pattern]
	return score




if DEBUG_EVAL:
	import win32gui
	def brain_eval(x, y):
		# TODO check if it works as expected
		wnd = win32gui.GetForegroundWindow()
		dc = win32gui.GetDC(wnd)
		rc = win32gui.GetClientRect(wnd)
		c = str(board[x][y])
		win32gui.ExtTextOut(dc, rc[2]-15, 3, 0, None, c, ())
		win32gui.ReleaseDC(wnd, dc)
class Node:
    def __init__(self, player = 1, successor = [], isLeaf = False, value = None, position:tuple = None):
        if player == 1:
            self.rule = 'max'
        else:
            self.rule = 'min'
        self.successor = successor
        self.isLeaf = isLeaf
        self.value = value
        self.position = position 

def value(node, alpha, beta):
    if node.rule == 'max':
        return maxValue(node, alpha, beta)
    else:
        return minValue(node, alpha, beta)


def maxValue(node, alpha, beta):
    if node.isLeaf:
        return node.value
    val = float("-inf")
    for action in node.successor:
        action.visited = True
        val = max(val, minValue(action, alpha, beta))
        if val >= beta:
            return val
        alpha = max(alpha, val)
    return val


def minValue(node, alpha, beta):
    if node.isLeaf:
        return node.value
    val = float("inf")
    for action in node.successor:
        action.visited = True
        val = min(val, maxValue(action, alpha, beta))
        if val <= alpha:
            return val
        beta = min(beta, val)
    return val


def constructTree(board, player, nodePosition):
    '''
    construct a tree using given information, and return the root node
    :param n:  the height of tree
    :param board: the input board described with list nested structure
    :param player: root node's type, 1 for max, 2 for min
    :return: root node
    '''
    node = Node(player=player)
    successors = []
    neighbors = findNeighbor(board)
    node.position = nodePosition
    for neighbor in neighbors:
        newboard = copy.deepcopy(board)
        position = (neighbor[0], neighbor[1])
        newboard[neighbor[0], neighbor[1]] = player
        if  score(newboard) > 5000:
            successors.append(Node(player=3-player, isLeaf=True, value=score(newboard), position=position))
        else:
            successors.append(constructTree(newboard, 3-player, nodePosition=position))
    node.successor = successors
    return node

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
if DEBUG_EVAL:
	pp.brain_eval = brain_eval

def main():
	pp.main()

if __name__ == "__main__":
	main()

