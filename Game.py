from cmu_graphics import *
from Board import *
from Piece import *
import random

b = Board(Side.WHITE)

Rook(4, 2, Side.WHITE, b)
Bishop(3, 6, Side.BLACK, b)

b.drawBoard()

def onMousePress(mx, my):
    b.selectTile(mx, my)
    b.drawBoard()

cmu_graphics.run()