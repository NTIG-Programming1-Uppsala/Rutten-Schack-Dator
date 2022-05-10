from cmu_graphics import *
from Board import *
from Piece import *

app.stepsPerSecond = 60

b = Board(Side.WHITE)

b.createPiece(4, 2, Type.ROOK, Side.WHITE)
b.createPiece(3, 6, Type.QUEEN, Side.BLACK)
b.createPiece(2, 3, Type.BISHOP, Side.BLACK)
b.createPiece(7, 3, Type.QUEEN, Side.WHITE)

b.createPiece(2, 7, Type.KING, Side.WHITE)

b.drawBoard()
b.initializeBoard()

def onMousePress(mx, my):
    b.selectTile(mx, my)
    b.drawBoard()

def onMouseMove(mx, my):
    x = mx // TILE_WIDTH
    y = my // TILE_HEIGHT

    # for w in range(BOARD_COLS):
    #     for z in range(BOARD_ROWS):
    #         b.tiles[w][z].glow = False
    #         if(w == x and y == z):
    #             b.tiles[w][z].glow = True
    # b.drawBoard()

def onKeyPress(key):
    if(key == 'r'):
        b.unMakePrevMove()
        b.drawBoard()

    if(key == 'space'):
        b.print()

cmu_graphics.run()