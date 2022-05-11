from cmu_graphics import *
from Board import *
from Piece import *

app.stepsPerSecond = 60

b = Board(Side.WHITE)

for i in range(BOARD_COLS):
    b.createPiece(i, 1, Type.PAWN, Side.BLACK)
    b.createPiece(i, 6, Type.PAWN, Side.WHITE)

b.createPiece(0, 0, Type.ROOK, Side.BLACK)
b.createPiece(7, 0, Type.ROOK, Side.BLACK)
b.createPiece(0, 7, Type.ROOK, Side.WHITE)
b.createPiece(7, 7, Type.ROOK, Side.WHITE)

b.createPiece(3, 0, Type.QUEEN, Side.BLACK)
b.createPiece(3, 7, Type.QUEEN, Side.WHITE)

b.createPiece(2, 0, Type.BISHOP, Side.BLACK)
b.createPiece(5, 0, Type.BISHOP, Side.BLACK)
b.createPiece(2, 7, Type.BISHOP, Side.WHITE)
b.createPiece(5, 7, Type.BISHOP, Side.WHITE)

b.createPiece(1, 0, Type.KNIGHT, Side.BLACK)
b.createPiece(6, 0, Type.KNIGHT, Side.BLACK)
b.createPiece(1, 7, Type.KNIGHT, Side.WHITE)
b.createPiece(6, 7, Type.KNIGHT, Side.WHITE)

b.createPiece(4, 0, Type.KING, Side.BLACK)
b.createPiece(4, 7, Type.KING, Side.WHITE)



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