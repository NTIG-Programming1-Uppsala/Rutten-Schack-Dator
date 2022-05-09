from cmu_graphics import *
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BOARD_COLS = 8
BOARD_ROWS = 8

TILE_WIDTH = 400/BOARD_COLS
TILE_HEIGHT = 400/BOARD_ROWS

DARK_TILE_COLOR = rgb(181, 136, 99)
LIGHT_TILE_COLOR = rgb(240, 217, 181)

dir_path = os.path.dirname(os.path.realpath(__file__))

w_queen = dir_path + '/Images/W_QUEEN.png'
w_king = dir_path + '/Images/W_KING.png'
w_rook = dir_path + '/Images/W_ROOK.png'
w_bishop = dir_path + '/Images/W_BISHOP.png'
w_knight = dir_path + '/Images/W_KNIGHT.png'
w_pawn = dir_path + '/Images/W_PAWN.png'

b_queen = dir_path + '/Images/B_QUEEN.png'
b_king = dir_path + '/Images/B_KING.png'
b_rook = dir_path + '/Images/B_ROOK.png'
b_bishop = dir_path + '/Images/B_BISHOP.png'
b_knight = dir_path + '/Images/B_KNIGHT.png'
b_pawn = dir_path + '/Images/B_PAWN.png'

PieceSprites = [
        w_pawn,
        b_pawn,
        w_knight,
        b_knight,
        w_bishop,
        b_bishop,
        w_rook,
        b_rook,
        w_queen,
        b_queen,
        w_king,
        b_king
]

def convertToCoords(x, y):
    coordX = TILE_WIDTH * (x + 1/2)
    coordY = TILE_HEIGHT * (y + 1/2)
    return coordX, coordY

def stepsToEdge(x, y, dirX, dirY):
    if(dirX == -1):
        if(dirY == 0):
            return x
        if(dirY == -1):
            return Clamp(0, y, x)
        if(dirY == 1):
            y = BOARD_ROWS - y - 1
            return Clamp(0, y, x)
    if(dirX == 1):
        if(dirY == 0):
            return BOARD_COLS - x - 1
        if(dirY == -1):
            x = BOARD_COLS - x - 1
            return Clamp(0, y, x)
        if(dirY == 1):
            x = BOARD_COLS - x - 1
            y = BOARD_ROWS - y - 1
            return Clamp(0, y, x)
    if(dirX == 0):
        if(dirY == -1):
            return y
        if(dirY == 1):
            return BOARD_ROWS - y - 1

def Clamp(min, max, value):
    if value > max:
        value = max
    if value < min:
        value = min
    
    return value