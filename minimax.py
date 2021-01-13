from itertools import product
import copy
from board_scorer import Scorer
from brain import logDebug

class Container:
    name = "container"

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
    def __init__(self, initialBoard, player, scorer:Scorer, nodePosition, maxDepth=10, currentDepth=0):
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
        self.board = initialBoard
        self.player = player

        self.firstMove = False
        if GomukuMinmaxTree.getStones(initialBoard, player) == GomukuMinmaxTree.getStones(initialBoard, 3-player):
            self.firstMove = True
        self.scorer.isFirstMove = self.firstMove
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
        value, pos = self.value(self.root, -float('inf'), float('inf'))
        #logDebug("[Take] [{},{}] with value = {}".format(pos[0], pos[1], value))
        #logDebug('[Evaluate Score] = {}'.format(self.scorer.evaluate(self.board, pos[0], pos[1], self.player)))
        return self.value(self.root, -float('inf'), float('inf'))

    # TODO Is The value really propagating up to parent nodes?
    def value(self, node, alpha, beta):
        if node.rule == 'max':
            return self.maxValue(node, alpha, beta)
        else:
            return self.minValue(node, alpha, beta)

    def maxValue(self, node, alpha, beta):
        if node.isLeaf:
            return node.value, node.position
        val = float("-inf")
        position = None
        for child in node.successor:
            child.visited = True
            childVal = self.minValue(child, alpha, beta)[0]
            if childVal > val:
                val = childVal
                position = child.position
            if val >= beta:  # Pruning
                return val, None
            alpha = max(alpha, val)
        return val, position

    def minValue(self, node, alpha, beta):
        if node.isLeaf:
            return node.value, node.position
        val = float("inf")
        position = None
        for child in node.successor:
            child.visited = True
            childVal = self.maxValue(child, alpha, beta)[0]

            if childVal < val:
                position = child.position
                val = childVal
            if val <= alpha:  # Pruning
                return val, None
            beta = min(beta, val)
        return val, position

    def constructTree(self, currentBoard, player, nodePosition, maxDepth=10, currentDepth=0):
        logDebug("Construct Tree with depth = {}".format(currentDepth))
        node = Node(player=player)
        successors = []
        neighbors = GomukuMinmaxTree.findNeighbor(currentBoard)

        # EXPLORAION_BRANCH = 30
        # if len(neighbors) > EXPLORAION_BRANCH:
        #     neighbors = neighbors[0: EXPLORAION_BRANCH]
        node.position = nodePosition

        expand_nodes = []
        for n in neighbors:
            container = Container()
            container.newboard = copy.deepcopy(currentBoard)
            container.newboard[n[0]][n[1]] = player
            container.position = (n[0], n[1])
            container.value = self.scorer.evaluate(container.newboard, n[0], n[1], player)
            expand_nodes.append(container)

        exploration_branch = 50
        if len(expand_nodes) > exploration_branch:
            expand_nodes = sorted(
                expand_nodes,
                key=lambda container: container.value,
                reverse=True
            )
        expand_nodes = expand_nodes[0:exploration_branch]

        for expand_node in expand_nodes:
            if currentDepth >= maxDepth or expand_node.value > 5000:
                successors.append(Node(player=3-player, isLeaf=True, value=expand_node.value, position=expand_node.position))
            else:
                successors.append(self.constructTree(
                    expand_node.newboard, player=3-player, nodePosition=expand_node.position,
                    maxDepth=maxDepth, currentDepth=currentDepth+1
                ))

        node.successor = successors
        return node

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