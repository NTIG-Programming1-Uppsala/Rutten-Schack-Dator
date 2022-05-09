
from cmu_graphics import *
from enum import Enum
from Settings import *
from Board import *

class Side(Enum):
    WHITE = 0
    BLACK = 1

class Type(Enum):
    PAWN = 0
    KNIGHT = 2
    BISHOP = 4
    ROOK = 6
    QUEEN = 8
    KING = 10

class Piece:
    def __init__(self, x, y, side, type, board):
        self.b = board

        self.x = x
        self.y = y

        self.b.tiles[x][y].piece = self

        self.side = side
        self.type = type

    def move(self, tile):
        self.x = tile.x
        self.y = tile.y

    def print(self):
        print()
        print('-------PIECE-------')
        print('Position: ', (self.x, self.y))
        print('Side: ', self.side)
        print('Type: ', self.type)
        print('-------PIECE-------')
        print()



class Rook(Piece):
    def __init__(self, x, y, side, board):
        super().__init__(x, y, side, Type.ROOK, board)

    def getPseudoLegalMoves(self):
        moves = []
        ### move[0] = startSquare ### move[1] == targetSquare ###

        for i in range(stepsToEdge(self.x, self.y, -1, 0)):
            move = (self.b.tiles[self.x][self.y], self.b.tiles[self.x - (i + 1)][self.y])
            if(self.b.pseudoLegalMove(move)):
                moves.append(move)
            else:
                break

        for i in range(stepsToEdge(self.x, self.y, 0, -1)):
            move = (self.b.tiles[self.x][self.y], self.b.tiles[self.x][self.y - (i + 1)])
            if(self.b.pseudoLegalMove(move)):
                moves.append(move)
            else:
                break

        for i in range(stepsToEdge(self.x, self.y, 1, 0)):
            move = (self.b.tiles[self.x][self.y], self.b.tiles[self.x + (i + 1)][self.y])
            if(self.b.pseudoLegalMove(move)):
                moves.append(move)
            else:
                break

        for i in range(stepsToEdge(self.x, self.y, 0, 1)):
            move = (self.b.tiles[self.x][self.y], self.b.tiles[self.x][self.y + (i + 1)])
            if(self.b.pseudoLegalMove(move)):
                moves.append(move)
            else:
                break

        return moves

class Bishop(Piece):
    def __init__(self, x, y, side, board):
        super().__init__(x, y, side, Type.BISHOP, board)

    def getPseudoLegalMoves(self):
        moves = []
        ### move[0] = startSquare ### move[1] == targetSquare ###

        for i in range(stepsToEdge(self.x, self.y, -1, -1)):
            move = (self.b.tiles[self.x][self.y], self.b.tiles[self.x - (i + 1)][self.y - (i + 1)])
            if(self.b.pseudoLegalMove(move)):
                moves.append(move)
            else:
                break

        for i in range(stepsToEdge(self.x, self.y, 1, -1)):
            move = (self.b.tiles[self.x][self.y], self.b.tiles[self.x + (i + 1)][self.y - (i + 1)])
            if(self.b.pseudoLegalMove(move)):
                moves.append(move)
            else:
                break

        for i in range(stepsToEdge(self.x, self.y, 1, 1)):
            move = (self.b.tiles[self.x][self.y], self.b.tiles[self.x + (i + 1)][self.y + (i + 1)])
            if(self.b.pseudoLegalMove(move)):
                moves.append(move)
            else:
                break

        for i in range(stepsToEdge(self.x, self.y, -1, 1)):
            move = (self.b.tiles[self.x][self.y], self.b.tiles[self.x - (i + 1)][self.y + (i + 1)])
            if(self.b.pseudoLegalMove(move)):
                moves.append(move)
            else:
                break

        return moves


