import random
from math import inf
from Piece import Side
import time

class ChessComputa:
    def __init__(self, depth, side, b):
        self.b = b
        self.side = side

        self.depth = depth
        self.num = 0
 
    def minimax(self, depth, alpha, beta, maxPlayer, maxColor): 

        legalMoves = self.b.getMoves(maxColor)

        if(depth == 0):
            return None, self.b.evaluate()

        random.shuffle(legalMoves)

        if(len(legalMoves) == 0):
            return None, self.b.evaluate()

        bestMove = random.choice(legalMoves)

        if(maxPlayer):
            # If max
            maxEval = -inf
            for move in legalMoves:
                self.b.makeMove(move)
                currentEval = self.minimax(depth - 1, alpha, beta, False, Side.WHITE)[1]
                self.b.unMakePrevMove()
                if(currentEval > maxEval):
                    maxEval = currentEval
                    bestMove = move
                alpha = max(alpha, currentEval)
                if(beta <= alpha):
                     break
            return bestMove, maxEval
        else:
            # If min
            minEval = inf
            for move in legalMoves:
                self.b.makeMove(move)
                currentEval = self.minimax(depth - 1, alpha, beta, True, Side.BLACK)[1]
                self.b.unMakePrevMove()
                if(currentEval < minEval):
                    minEval = currentEval
                    bestMove = move
                beta = min(beta, currentEval)
                if(beta <= alpha):
                    break    
            return bestMove, minEval