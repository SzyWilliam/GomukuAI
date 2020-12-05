from itertools import product
import copy
from board_scorer import Scorer


class Node:
    """
    Definition for each node in the minmax Tree
    """
    def __init__(self, player=1, successor=[], isLeaf=False, value=None, position: tuple = None):
        """
        :param player: 1 means the max, 2 means the min
        :param successor: children nodes
        :param isLeaf:
        :param value: the evaluation for the this node
        :param position: when state transfer from Self.Parent -> Self, on which position should the next move be put
        """
        if player == 1:
            self.rule = 'max'
        else:
            self.rule = 'min'
        self.successor = successor
        self.isLeaf = isLeaf
        self.value = value
        self.position = position


class GomukuMinmaxTree:
    def __init__(self, initialBoard, player, scorer: Scorer, nodePosition, maxDepth=10, currentDepth=0):
        """
        Construct a minmax Tree for Gomuku problem
        :param initialBoard:
        :param player:
        :param scorer:
        :param nodePosition:
        :param maxDepth:
        :param currentDepth:
        """
        self.scorer = scorer
        self.root = self.constructTree(
            initialBoard,
            player,
            nodePosition,
            maxDepth,
            0
        )

    def solveMinmaxWithABPruning(self):
        """
        Solve The initialBoard with Minmax (ABPruning)
        :return: a tuple, first element is the max value calculated for current board
            second element is the position of the best move
        """
        root_value = self.value(self.root, -float('inf'), float('inf'))
        nextPosition = None
        for succ in self.root.successor:
            if succ.value == root_value:
                nextPosition = succ.position
                break
        return root_value, nextPosition

    def value(self, node, alpha, beta):
        if node.rule == 'max':
            return self.maxValue(node, alpha, beta)
        else:
            return self.minValue(node, alpha, beta)

    def maxValue(self, node, alpha, beta):
        if node.isLeaf:
            return node.value
        val = float("-inf")
        for action in node.successor:
            action.visited = True
            val = max(val, self.minValue(action, alpha, beta))
            if val >= beta:
                node.value = val  # Propagation
            alpha = max(alpha, val)
        return val

    def minValue(self, node, alpha, beta):
        if node.isLeaf:
            return node.value
        val = float("inf")
        for action in node.successor:
            action.visited = True
            val = min(val, self.maxValue(action, alpha, beta))
            if val <= alpha:
                node.value = val
            beta = min(beta, val)
        return val

    def constructTree(self, currentBoard, player, nodePosition, maxDepth=10, currentDepth=0):
        node = Node(player=player)
        successors = []
        neighbors = GomukuMinmaxTree.findNeighbor(currentBoard)
        node.position = nodePosition
        for neighbor in neighbors:
            newboard = copy.deepcopy(currentBoard)
            position = (neighbor[0], neighbor[1])
            newboard[neighbor[0]][neighbor[1]] = player
            if self.scorer.evaluate(newboard) > 5000 or currentDepth >= maxDepth:
                successors.append(Node(player=3 - player, isLeaf=True,
                                       value=self.scorer.evaluate(newboard), position=position))
            else:
                successors.append(self.constructTree(newboard, player=3 - player, nodePosition=position,
                                                                 maxDepth=maxDepth, currentDepth=currentDepth + 1))
        node.successor = successors
        return node

    @staticmethod
    def findNeighbor(board, neighborNearBy=3):
        """
        Find all open positions less than 3 cells away
        TODO Enable more general neighbor discovering strategy
        :param board:
        :param neighborNearBy: how much distance
        :return: a list of binary tuples.
        """
        neighbors = []
        getStones = GomukuMinmaxTree.getStones
        stones = getStones(board, 1) + getStones(board, 2)
        for stone in stones:
            for i, j in product(range(stone[0] - 1, stone[0] + 2), range(stone[1] - 1, stone[1] + 2)):
                if (i, j) in product(range(len(board)), range(len(board))) and (i, j) not in neighbors and (
                        i, j) not in stones:
                    neighbors.append((i, j))
        return neighbors

    @staticmethod
    def getStones(board, player):
        """
        Find all stones of the given player
        :returns a list of binary tuples.
        """
        stones = [(i, j) for i in range(len(board)) for j in range(len(board)) if board[i][j] == player]
        return stones