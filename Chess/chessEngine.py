class GameState:
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'B': self.getBishopMoves,
                              'N': self.getKnightMoves, 'K': self.getKingMoves, 'Q': self.getQueenMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.empassantPossible = ()
        self.empassantPossibleLog = [self.empassantPossible]
        self.wQueenCastlingPossible = True
        self.bQueenCastlingPossible = True
        self.wKingCastlingPossible = True
        self.bKingCastlingPossible = True

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "  "
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)

        if move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"

        if move.isEmpassantMove:
            self.board[move.startRow][move.endCol] = "  "

        if move.pieceMoved[1] == "P" and abs(move.startRow - move.endRow) == 2:
            self.empassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.empassantPossible = ()

        length = len(self.moveLog)
        if move.isCastling:

            if move.pieceMoved == "wK":
                if move.endCol == 6:
                    self.board[7][5] = "wR"
                    self.board[7][7] = "  "
                else:
                    self.board[7][3] = "wR"
                    self.board[7][0] = "  "

            else:
                if move.endCol == 6:
                    self.board[0][5] = "bR"
                    self.board[0][7] = "  "
                else:
                    self.board[0][3] = "bR"
                    self.board[0][0] = "  "

        if move.pieceMoved == "wK":

            if self.wKingCastlingPossible:
                self.wKingCastlingPossible = False
                self.moveLog[length - 1].notWKSCastling = True

            if self.wQueenCastlingPossible:
                self.wQueenCastlingPossible = False
                self.moveLog[length - 1].notWQSCastling = True
        elif move.pieceMoved == "bK":

            if self.bKingCastlingPossible:
                self.bKingCastlingPossible = False
                self.moveLog[length - 1].notBKSCastling = True
            if self.bQueenCastlingPossible:
                self.bQueenCastlingPossible = False
                self.moveLog[length - 1].notBQSCastling = True
        if self.wKingCastlingPossible and self.board[7][7] != "wR":
            self.wKingCastlingPossible = False
            self.moveLog[length - 1].notWKSCastling = True

        if self.wQueenCastlingPossible and self.board[7][0] != "wR":
            self.wQueenCastlingPossible = False
            self.moveLog[length - 1].notWQSCastling = True
        if self.bKingCastlingPossible and self.board[0][7] != "bR":
            self.bKingCastlingPossible = False
            self.moveLog[length - 1].notBKSCastling = True
        if self.bQueenCastlingPossible and self.board[0][0] != "bR":
            self.bQueenCastlingPossible = False
            self.moveLog[length - 1].notBQSCastling = True

        self.empassantPossibleLog.append(self.empassantPossible)

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)

            if move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            if move.isEmpassantMove:
                self.board[move.endRow][move.endCol] = "  "
                self.board[move.startRow][move.endCol] = move.pieceCaptured

            self.empassantPossibleLog.pop()
            self.empassantPossible = self.empassantPossibleLog[-1]

            if move.isCastling:
                if move.pieceMoved == "wK" and move.endCol == 6:
                    self.board[7][5] = "  "
                    self.board[7][7] = "wR"
                elif move.pieceMoved == "wK":
                    self.board[7][3] = "  "
                    self.board[7][0] = "wR"
                elif move.pieceMoved == "bK" and move.endCol == 6:
                    self.board[0][5] = "  "
                    self.board[0][7] = "bR"
                else:
                    self.board[0][3] = "  "
                    self.board[0][0] = "bR"

            if move.notWQSCastling:
                self.wQueenCastlingPossible = True
            if move.notWKSCastling:
                self.wKingCastlingPossible = True

            if move.notBKSCastling:
                self.bKingCastlingPossible = True
            if move.notBQSCastling:
                self.bQueenCastlingPossible = True

            self.checkMate = False
            self.staleMate = False

    def getValidMoves(self):

        tempEmpassantPossible = self.empassantPossible
        moves = self.getAllPossibleMoves()
        for i in range(len(moves) - 1, -1, -1):

            self.makeMove(moves[i])

            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        self.empassantPossible = tempEmpassantPossible
        moves = self.checkCastling(moves)
        return moves

    def checkCastling(self, moves):

        if self.whiteToMove and self.wKingCastlingPossible:
            if not self.squareUnderAttack(7, 4):
                if self.board[7][5] == "  " and not self.squareUnderAttack(7, 5):
                    if self.board[7][6] == "  " and not self.squareUnderAttack(7, 6):
                        moves.append(Move((7, 4), (7, 6), self.board, isCastling=True))
        if self.whiteToMove and self.wQueenCastlingPossible:
            if not self.squareUnderAttack(7, 4):
                if self.board[7][3] == "  " and not self.squareUnderAttack(7, 3):
                    if self.board[7][2] == "  " and not self.squareUnderAttack(7, 2):
                        if self.board[7][1] == "  ":
                            moves.append(Move((7, 4), (7, 2), self.board, isCastling=True))

        if not self.whiteToMove and self.bKingCastlingPossible:
            if not self.squareUnderAttack(0, 4):
                if self.board[0][5] == "  " and not self.squareUnderAttack(0, 5):
                    if self.board[0][6] == "  " and not self.squareUnderAttack(0, 6):
                        moves.append(Move((0, 4), (0, 6), self.board, isCastling=True))

        if not self.whiteToMove and self.bQueenCastlingPossible:
            if not self.squareUnderAttack(0, 4):
                if self.board[0][3] == "  " and not self.squareUnderAttack(0, 3):
                    if self.board[0][2] == "  " and not self.squareUnderAttack(0, 2):
                        if self.board[0][1] == "  ":
                            moves.append(Move((0, 4), (0, 2), self.board, isCastling=True))

        return moves

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove

        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):

                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)

        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:

            if self.board[r - 1][c] == "  ":
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "  ":
                    moves.append(Move((r, c), (r - 2, c), self.board))

            if c > 0:
                if self.board[r - 1][c - 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.empassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEmpassantMove=True))
            if c < len(self.board) - 1:
                if self.board[r - 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.empassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEmpassantMove=True))

        else:
            if self.board[r + 1][c] == "  ":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "  ":
                    moves.append(Move((r, c), (r + 2, c), self.board))

            if c > 0:
                if self.board[r + 1][c - 1][0] == "w":

                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.empassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEmpassantMove=True))
            if c < len(self.board) - 1:
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.empassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEmpassantMove=True))

    def getRookMoves(self, r, c, moves):
        directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        color = self.board[r][c][0]
        for x, y in directions:
            for i in range(1, len(self.board)):

                posX = x * i + r
                posY = y * i + c
                if posX < 0 or posX == len(self.board) or posY < 0 or posY == len(self.board):
                    break
                elif self.board[posX][posY] == "  ":
                    moves.append(Move((r, c), (posX, posY), self.board))
                elif self.board[posX][posY][0] == color:
                    break
                else:
                    moves.append(Move((r, c), (posX, posY), self.board))
                    break

    def getBishopMoves(self, r, c, moves):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        color = self.board[r][c][0]
        for x, y in directions:
            for i in range(1, len(self.board)):

                posX = x * i + r
                posY = y * i + c
                if posX < 0 or posX == len(self.board) or posY < 0 or posY == len(self.board):
                    break
                elif self.board[posX][posY] == "  ":
                    moves.append(Move((r, c), (posX, posY), self.board))
                elif self.board[posX][posY][0] == color:
                    break
                else:
                    moves.append(Move((r, c), (posX, posY), self.board))
                    break

    def getKnightMoves(self, r, c, moves):
        color = self.board[r][c][0]
        directions = [(2, 1), (1, 2), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
        for x, y in directions:
            posX = r + x
            posY = c + y
            if posX < 0 or posX >= len(self.board) or posY < 0 or posY >= len(self.board):
                continue
            elif self.board[posX][posY] == "  " or self.board[posX][posY][0] != color:
                moves.append(Move((r, c), (posX, posY), self.board))

    def getKingMoves(self, r, c, moves):
        color = self.board[r][c][0]
        directions = [(1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]
        for x, y in directions:
            posX = r + x
            posY = c + y
            if posX < 0 or posX >= len(self.board) or posY < 0 or posY >= len(self.board):
                continue
            elif self.board[posX][posY] == "  " or self.board[posX][posY][0] != color:
                moves.append(Move((r, c), (posX, posY), self.board))

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)


class Move:
    ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {'h': 7, 'g': 6, 'f': 5, 'e': 4, 'd': 3, 'c': 2, 'b': 1, 'a': 0}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEmpassantMove=False, isCastling=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        self.isPawnPromotion = self.pieceMoved == "wP" and self.endRow == 0 or self.pieceMoved == "bP" and self.endRow == 7

        self.isEmpassantMove = isEmpassantMove
        if self.isEmpassantMove:
            self.pieceCaptured = "wP" if self.pieceMoved == "bP" else "bP"

        self.isCastling = isCastling
        self.notWQSCastling = False
        self.notWKSCastling = False
        self.notBQSCastling = False
        self.notBKSCastling = False

        self.isCapture = self.pieceCaptured != "  "

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def __str__(self):
        if self.isCastling:
            return "0-0" if self.endCol == 6 else "0-0-0"

        endSquare = self.getRankFile(self.endRow, self.endCol)

        if self.pieceMoved[1] == "P":
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare

            #pawnPromotion

        #adding check and checkmate

        moveString=self.pieceMoved[1]
        if self.isCapture:
            moveString+="x"
        return moveString+endSquare
