from cmu_graphics import *
from Board import *
from Piece import *

b = Board(Side.WHITE)

Rook(4, 2, Side.WHITE, b)
Bishop(3, 6, Side.BLACK, b)
Queen(2, 7, Side.BLACK, b)
Queen(7, 3, Side.WHITE, b)

b.drawBoard()

def onMousePress(mx, my):
    b.selectTile(mx, my)
    b.drawBoard()

def onMouseMove(mx, my):
    x = mx // TILE_WIDTH
    y = my // TILE_HEIGHT

    for w in range(BOARD_COLS):
        for z in range(BOARD_ROWS):
            b.tiles[w][z].glow = False
            if(w == x and y == z):
                b.tiles[w][z].glow = True

    b.drawBoard()


cmu_graphics.run()