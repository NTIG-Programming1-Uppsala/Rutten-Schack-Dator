from Settings import *
from cmu_graphics import *
from Piece import *

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.piece = None

        self.glowColor = None

        self.checkedBy = []

    def print(self) -> str:
        print('   -------TILE---------')
        print('   X: ', self.x)
        print('   Y: ', self.y)
        print('   Checked by: ', )
        for p in self.checkedBy:
            p.print()
        if(self.piece):
            print('   Piece On Tile: ')
            self.piece.print()
        else:
            print('   Piece On Tile: ', self.piece)
        print('   -------TILE---------')

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

        self.inCheck = None

        self.pieces = []

        self.blackKingTile = None
        self.whiteKingTile = None

        self.selected = None
        self.turn = Side.WHITE

    def print(self):
        print('-------BOARD-------')
        for x in range(BOARD_COLS):
            for y in range(BOARD_ROWS):
                print('-----')
                self.tiles[x][y].print()
        print('-----')
        print('In Check: ', self.inCheck)
        if(self.selected):
            print('Current Selected Square:')
            self.selected.print()
        else:
            print('Current Selected Square: ', self.selected)
        print('Current Turn: ', self.turn)
        print('TileSprites: ', len(self.tileSprites))
        print('PieceSprites: ', len(self.pieceSprites))
        print('Pieces On Board: ', len(self.pieces))

        if(self.blackKingTile):
            print('Black King Tile:')
            self.blackKingTile.print()
        else:
            print('Black King Tile: ', self.blackKingTile)
        
        if(self.whiteKingTile):
            print('White King Tile:')
            self.whiteKingTile.print()
        else:
            print('White King Tile: ', self.whiteKingTile)

        print('-------BOARD-------')


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
                elif(self.selected and self.selected.piece and self.tiles[x][y] in [i[1] for i in self.selected.piece.getLegalMoves()]):
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

    def initializeBoard(self):
        self.calculateCheckedTiles()

    def createPiece(self, x, y, type, side):
        if(type == Type.PAWN):
            pass
            #self.tiles[x][y].piece = Pawn(x, y, side, self)
        elif(type == Type.KNIGHT):
            pass
            #self.tiles[x][y].piece = Knight(x, y, side, self)
        elif(type == Type.BISHOP):
            self.tiles[x][y].piece = Bishop(x, y, side, self)
        elif(type == Type.ROOK):
            self.tiles[x][y].piece = Rook(x, y, side, self)
        elif(type == Type.QUEEN):
            self.tiles[x][y].piece = Queen(x, y, side, self)
        elif(type == Type.KING):
            self.tiles[x][y].piece = King(x, y, side, self)
            if(side == Side.BLACK):
                self.blackKingTile = self.tiles[x][y]
            elif(side == Side.WHITE):
                self.whiteKingTile = self.tiles[x][y]

        self.pieces.append(self.tiles[x][y].piece)

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
            if(tryMove in self.selected.piece.getLegalMoves()):
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

    def coordsAreInBounds(self, coords):
        x = coords[0]
        y = coords[1]
        if(x >= 0 and x <= BOARD_COLS-1 and y >= 0 and y <= BOARD_ROWS-1):
            return True
        return False

    def hasEnemyOnTile(self, tile, side):
        if(self.hasPieceOnTile(tile) and tile.piece.side != side):
            return True
        return False

    def getMovesInLine(self, startTile, endTile):
        dirX = endTile.x - startTile.x
        dirY = endTile.y - startTile.y

        if(abs(dirX) != abs(dirY) and abs(dirX) != 0 and abs(dirY) != 0):
            return False, []

        piece = self.tiles[startTile.x][startTile.y].piece

        if(piece.type == Type.BISHOP and (dirX == 0 or dirY == 0)):
            return False, []
        elif(piece.type == Type.ROOK and (dirX != 0 or dirY != 0)):
            return False, []

        if(dirX == 0):
            steps = abs(dirY)
        elif(dirY == 0):
            steps = abs(dirX)
        else:
            steps = abs(dirX)

        dirX = sign(dirX)
        dirY = sign(dirY)

        moves = []
        for i in range(steps - 1):
            move = self.tiles[startTile.x + dirX * (i + 1)][startTile.y + dirY * (i + 1)]
            moves.append(move)

        return True, moves

    def isLegalMove(self, move):
        startTile = move[0]
        targetTile = move[1]
        movingPiece = startTile.piece
            
        if(movingPiece.type == Type.KING):
            for piece in targetTile.checkedBy:
                if(piece.side != movingPiece.side):
                    return False
            return True
        else:
            if(movingPiece.side == Side.BLACK):
                king = self.blackKingTile
            elif(movingPiece.side == Side.WHITE):
                king = self.whiteKingTile
            if(not king):
                return True

            allowed = True
            for piece in self.pieces:
                if(piece.side != movingPiece.side and (piece.type == Type.BISHOP or piece.type == Type.ROOK or piece.type == Type.QUEEN)):
                    pieceTile = self.tiles[piece.x][piece.y]
                    hasLine, lineMoves = self.getMovesInLine(pieceTile, king)
                    if(hasLine):
                        protPieces = []
                        for m in lineMoves:
                            if(m.piece):
                                protPieces.append(m.piece)
                        if(len(protPieces) == 0):
                            if(len(king.checkedBy) > 1):
                                if(movingPiece.type == Type.ROOK):
                                    piece.print()
                                return False
                            if(targetTile not in lineMoves and targetTile != pieceTile):
                                if(movingPiece.type == Type.ROOK):
                                    print('target:')
                                    targetTile.print()
                                    print('pieceTile:')
                                    pieceTile.print()
                                return False
                        if(movingPiece in protPieces):
                            if(targetTile not in lineMoves):
                                if(targetTile != pieceTile):
                                    if(len(protPieces) == 1):
                                        return False
            return True

            if(allowed):
                return True
            return False
            
            if(self.inCheck and self.inCheck.side == movingPiece.side):
                kingTile = self.tiles[self.inCheck.x][self.inCheck.y]
                for piece in kingTile.checkedBy:
                    if(targetTile == self.tiles[piece.x][piece.y] and len(kingTile.checkedBy) == 1):
                        return True
                    if((piece.type == Type.BISHOP or piece.type == Type.ROOK or piece.type == Type.QUEEN) and targetTile in self.getMovesInLine(self.tiles[piece.x][piece.y], kingTile)[1]):
                        return True
                return False 

            if(allowedMove):
                return True
            return False

    def isPseudoLegalMove(self, move):
        startTile = move[0]
        targetTile = move[1]

        if(not self.hasPieceOnTile(targetTile) or self.hasEnemyOnTile(targetTile, startTile.piece.side)):
            return True
        return False

    def calculateCheckedTiles(self):
        self.inCheck = None

        for x in range(BOARD_COLS):
            for y in range(BOARD_ROWS):
                self.tiles[x][y].checkedBy = []

        for x in range(BOARD_COLS):
            for y in range(BOARD_ROWS):     
                piece = self.tiles[x][y].piece
                if(piece):
                    for move in piece.getPseudoLegalMoves():
                        move[1].checkedBy.append(piece)
                        if(move[1].piece and move[1].piece.type == Type.KING):
                            self.inCheck = move[1].piece

    def makeMove(self, move):
        startTile = move[0]
        targetTile = move[1]

        previousState = {
            "startTile": (startTile, startTile.copy()),
            "targetTile": (targetTile, targetTile.copy()),
            }

        self.previousMoves.append(previousState)

        movingPiece = startTile.piece
        
        startTile.piece = None
        startTile.selected = False


        movingPiece.move(targetTile)
        if(movingPiece.type == Type.KING):
            if(movingPiece.side == Side.BLACK):
                self.blackKingTile = targetTile
            elif(movingPiece.side == Side.WHITE):
                self.whiteKingTile = targetTile
                
        if(targetTile.piece):
            self.pieces.remove(targetTile.piece)

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

            self.pieces.append(self.tiles[startTileX][startTileY].piece)

            if(self.tiles[startTileX][startTileY].piece.type == Type.KING):
                if(self.tiles[startTileX][startTileY].piece.side == Side.BLACK):
                    self.blackKingTile = self.tiles[startTileX][startTileY]
                elif(self.tiles[startTileX][startTileY].piece.side == Side.WHITE):
                    self.whiteKingTile = self.tiles[startTileX][startTileY]
                

            targetTileX = prevState["targetTile"][0].x
            targetTileY = prevState["targetTile"][0].y
            self.tiles[targetTileX][targetTileY] = prevState["targetTile"][1]

            self.calculateCheckedTiles()

            self.nextTurn()
        else:
            print('No Previous Moves Availabe')



        
