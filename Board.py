from tkinter.messagebox import NO
from tracemalloc import start
from Settings import *
from cmu_graphics import *
from Piece import Side


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.piece = None

        self.glowColor = None

        self.checkedBy = []

    def setGlowColor(self, color):
        self.glowColor = color

    def print(self) -> str:
        print('-------TILE---------')
        print('X: ', self.x)
        print('Y: ', self.y)
        print('Piece On Tile: ', self.piece)
        print('Checked by: ', self.checkedBy)
        print('-------TILE---------')

    def copy(self):
        piece = None
        if(self.piece):
            piece = self.piece.copy()
        copy = Tile(self.x, self.y)
        copy.piece = piece
        copy.checkedBy = self.checkedBy
        copy.glowColor = self.glowColor
        return copy

class Board:
    def __init__(self, playerSide):
        self.tiles = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

        self.initializeTiles()

        self.playerSide = playerSide

        self.pieceSprites = []
        self.tileSprites = []

        self.previousMoves = []

        self.selected = None
        self.turn = Side.WHITE

    def drawBoard(self):
        
        for sprite in self.tileSprites:
            sprite.visible = False

        self.tileSprites = []

        for sprite in self.pieceSprites:
            sprite.visible = False

        self.pieceSprites = []

        for x in range(BOARD_COLS):
            for y in range(BOARD_ROWS):
                if(self.selected == self.tiles[x][y]):
                    color = HIGHLIGHTED_TILE_COLOR
                # For debugging
                # elif(len(self.tiles[x][y].checkedBy) != 0):
                #     if((x + y) % 2 == 0):
                #         color = LIGHT_ALLOWEDMOVE_TILE_COLOR
                #     else:
                #         color = DARK_ALLOWEDMOVE_TILE_COLOR
                elif(self.selected and self.selected.piece in self.tiles[x][y].checkedBy):
                    if((x + y) % 2 == 0):
                        color = LIGHT_ALLOWEDMOVE_TILE_COLOR
                    else:
                        color = DARK_ALLOWEDMOVE_TILE_COLOR
                else:
                    if((x + y) % 2 == 0):
                        color = LIGHT_TILE_COLOR
                    else:
                        color = DARK_TILE_COLOR
                self.tileSprites.append(Rect(x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT, fill=color))

                piece = self.tiles[x][y].piece
                coords = convertToCoords(x, y)
                if(piece):
                    if(piece.side is Side.WHITE):
                        piece.b.pieceSprites.append(Image(PieceSprites[piece.type.value], coords[0] - TILE_WIDTH/2, coords[1] - TILE_HEIGHT/2, width=TILE_WIDTH, height=TILE_HEIGHT))
                    else:
                        piece.b.pieceSprites.append(Image(PieceSprites[piece.type.value + 1], coords[0] - TILE_WIDTH/2, coords[1] - TILE_HEIGHT/2, width=TILE_WIDTH, height=TILE_HEIGHT))

    def initializeTiles(self):
        for x in range(BOARD_COLS):
            for y in range(BOARD_ROWS):
                self.tiles[x][y] = Tile(x, y)

    def print(self):
        print('-------BOARD-------')
        for x in range(BOARD_COLS):
            for y in range(BOARD_ROWS):
                print('-----')
                print('Tile: ', (self.tiles[x][y].x, self.tiles[x][y].y))
                print('Piece on tile: ', self.tiles[x][y].piece)
        print('-----')
        print('-------BOARD-------')

    def selectTile(self, mx, my):

        if(self.playerSide != self.turn):
            return

        mouseX = mx // TILE_WIDTH
        mouseY = my // TILE_HEIGHT

        x = int(mouseX)
        y = int(mouseY)

        mouseTile = self.tiles[x][y]

        # Check if piece is selected. If so, make move if legal
        if self.selected:
            tryMove = (self.selected, mouseTile)
            if(tryMove in self.selected.piece.getPseudoLegalMoves()):
                #and not self.in_check_after_move(self.selected, coords,
                                                 #self.selected.piece.color):
                self.makeMove((self.selected, mouseTile))
                self.selected = None
                ## NEXT TURN ###
                return

        # If we click outside any legal moves, deselect the current selected tile
        if self.selected:
            self.selected = None

        # If we click on a tile which has a piece of our color, select it
        if(self.hasPieceOnTile(mouseTile) and mouseTile.piece.side == self.turn):
            self.selected = mouseTile

    def nextTurn(self):
        if(self.turn == Side.WHITE):
            self.turn = Side.BLACK
        else:
            self.turn = Side.WHITE

        # If no AI:
        if(self.playerSide == Side.WHITE):
            self.playerSide = Side.BLACK
        else:
            self.playerSide = Side.WHITE
        
    def hasPieceOnTile(self, tile):
        if(tile.piece):
            return True
        return False

    def enemyIsOnTile(self, tile, side):
        if(self.hasPieceOnTile(tile) and tile.piece.side != side):
            return True
        return False

    def pseudoLegalMove(self, move):
        startTile = move[0]
        targetTile = move[1]

        if(not self.hasPieceOnTile(targetTile) or self.enemyIsOnTile(targetTile, startTile.piece.side)):
            return True
        return False

    def calculateCheckedTiles(self):
        for x in range(BOARD_COLS):
            for y in range(BOARD_ROWS):
                self.tiles[x][y].checkedBy = []

        for x in range(BOARD_COLS):
            for y in range(BOARD_ROWS):     
                piece = self.tiles[x][y].piece
                if(piece):
                    for move in piece.getPseudoLegalMoves():
                        move[1].checkedBy.append(piece)

    def makeMove(self, move):

        startTile = move[0]
        targetTile = move[1]

        previousState = {
            "startTile": (startTile, startTile.copy()),
            "targetTile": (targetTile, targetTile.copy())
            }

        self.previousMoves.append(previousState)

        movingPiece = startTile.piece
        targetPiece = targetTile.piece
        
        startTile.piece = None
        startTile.selected = False


        movingPiece.move(targetTile)
        targetTile.piece = movingPiece
        
        ### CHECK FOR PAWN PROMOTION ###

        ### CHECK FOR CHECKMATE ###
        ### CHECH FOR STALEMATE ###

        self.calculateCheckedTiles()

        self.nextTurn()

    def unMakePrevMove(self):
        if(len(self.previousMoves) != 0):
            prevState = self.previousMoves.pop()

            startTileX = prevState["startTile"][0].x
            startTileY = prevState["startTile"][0].y
            self.tiles[startTileX][startTileY] = prevState["startTile"][1]

            targetTileX = prevState["targetTile"][0].x
            targetTileY = prevState["targetTile"][0].y
            self.tiles[targetTileX][targetTileY] = prevState["targetTile"][1]

            self.calculateCheckedTiles()

            self.nextTurn()



        
