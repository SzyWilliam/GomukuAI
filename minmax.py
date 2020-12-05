"""
Minmax with abPruning
(Based on lab2)
"""
from brain import getStones,findNeighbor,score
import copy

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
        newboard[position] = player
        if  score(newboard) == 5000:
            successors.append(Node(player=3-player, isLeaf=True, value=5000, position=position))
        else:
            successors.append(constructTree(newboard, 3-player, nodePosition=position))
    node.successor = successors
    return node