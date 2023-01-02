# engine.py
class Engine:
    """
    Based on FEN requirements
    To Do: Half move clock
    - Since last capture or pawn move
    To Do: Full move number
    - Increments after blacks move

    To Do:
    fix issues with king position, we're losing the kings every once in a while

    Saved FEN positions
    - start position: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
    - endgame: 8/8/8/8/5R2/2pk4/5K2/8 b - - 0 1
    """
    def __init__(self):
        # --- Board Representation --- #
        self.fenString = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        # --- Turns --- #
        self.whiteToMove = True
        if self.whiteToMove:
            self.player = "e"
        else:
            self.player = "k"

        # --- King State --- #
        self.whiteKingCoords = (7, 4)
        self.blackKingCoords = (0, 4)

        self.whiteCastling = {"kingside": False, "queenside": False}
        self.blackCastling = {"kingside": False, "queenside": False}

        # --- Google En Passant --- #
        self.enPassantPossibleWhite = False
        self.enPassantPossibleBlack = False

        # --- Game Conditions --- #
        self.isMate = False
        self.isStalemate = False

        # --- Set Up Board --- #
        self.virtualBoard = self.boardFromFEN()

        # --- Move Tracker --- #
        self.moveLog = []

    def makeMove(self, move):
        if move.startRank == move.endRank and move.startFile == move.endFile:
            pass
        else:
            # Basic Move Making
            self.virtualBoard[move.startRank][move.startFile] = "0"
            self.virtualBoard[move.endRank][move.endFile] = move.pieceMoved
            self.moveLog.append(move)

            # Switch Turns
            self.whiteToMove = not self.whiteToMove

            # Pawn Promotion
            if move.pawnPromotion:
                if self.whiteToMove:
                    self.virtualBoard[move.endRank][move.endFile] = "queen_black"
                else:
                    self.virtualBoard[move.endRank][move.endFile] = "queen_white"

            # En Passant
            if move.enPassant:
                print("possible en passant")

            # King Moves
            self.updateKings(move)

    def takeback(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.virtualBoard[move.startRank][move.startFile] = move.pieceMoved
            self.virtualBoard[move.endRank][move.endFile] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

            # Update King locations
            self.updateKings(move)
        else:
            print("No moves to undo")

    def findPieceLegalMoves(self):
        legalMoves = []

        for file in range(len(self.virtualBoard)):
            for rank in range(len(self.virtualBoard[file])):
                self.player = self.virtualBoard[rank][file][-1]

                # White ends in an e, black in a k
                if self.player == "e" and self.whiteToMove or self.player == "k" and not self.whiteToMove:
                    pieceType = self.virtualBoard[rank][file][0]  # p-pawn, k-knight, b-bishop, r-rook, q-queen, K-king

                    if pieceType == "p":
                        self.getPawnMoves(rank, file, legalMoves)
                    elif pieceType == "k":
                        self.getKnightMoves(rank, file, legalMoves)
                    elif pieceType == "b":
                        self.getBishopMoves(rank, file, legalMoves)
                    elif pieceType == "r":
                        self.getRookMoves(rank, file, legalMoves)
                    elif pieceType == "q":
                        self.getQueenMoves(rank, file, legalMoves)
                    elif pieceType == "K":
                        self.getKingMoves(rank, file, legalMoves)

        return legalMoves

    def generateMoves(self, psuedoLegal):
        """
        Removes illegal moves from the list of possible piece moves in the current position
        :param psuedoLegal:
        :return:
        """
        legal = []
        """
        Basic legal moves:
        1. Generate all possible legal moves
        2. Make each move
        3. Generate all of opponents moves
        4. If any of those moves take the king: prune the move
        """

        """
        Check logic
        We have each kings coordinates, if those coordinates are a valid move for the other team, the king is
        in check and must do something about it.
        
        check each of the opponent's next legal moves to see they could take the king
        
        1. switch to opponent's turn
            2. generateMoves and store in a variable
            3. if any of those moves could take the king, then it is a check, otherwise false
        """
        # castling goes here

        # --- Pruning Illegal Moves --- #
        for move in psuedoLegal:
            self.makeMove(move)
            oppMoves = self.findPieceLegalMoves()

            self.whiteToMove = not self.whiteToMove

            if not self.check(oppMoves):
                legal.append(move)

            self.whiteToMove = not self.whiteToMove
            self.takeback()

        # --- Game Ends by Checkmate or Stalemate --- #
        if len(legal) == 0:
            self.whiteToMove = not self.whiteToMove
            oppMoves = self.findPieceLegalMoves()
            self.whiteToMove = not self.whiteToMove

            if self.check(oppMoves):
                print("checkmate")
            else:
                print("stalemate")

        # --- En Passant Here --- #

        # Had this line before, now it breaks something, hopefully, deleting it won't break something
        # if len(self.moveLog) > 0:
        #     if self.moveLog[-1].twoSquareAdvance and self.whiteToMove:
        #         pass

        return legal

    def check(self, oppMoves):
        """
        Determines if possible moves will be illegal
        :param oppMoves: arr (list of move objects to be evaluated)
        :return: bool (True if player is in check, False otherwise)
        """
        if self.whiteToMove:
            for move in oppMoves:
                if move.endRank == self.whiteKingCoords[0] and move.endFile == self.whiteKingCoords[1]:
                    return True
            return False
        for move in oppMoves:
            if move.endRank == self.blackKingCoords[0] and move.endFile == self.blackKingCoords[1]:
                return True
        return False

    def moveIsCheck(self, move):
        """
        Determines if a single move is a check
        :param move: Move Object
        :return: True if move is a check, False otherwise
        """
        moves = []

        piece = move.pieceMoved[:1]

        if piece == "p":
            self.getPawnMoves(move.endRank, move.endFile, moves)
        elif piece == "k":
            self.getKnightMoves(move.endRank, move.endFile, moves)
        elif piece == "b":
            self.getBishopMoves(move.endRank, move.endFile, moves)
        elif piece == "r":
            self.getRookMoves(move.endRank, move.endFile, moves)
        elif piece == "q":
            self.getQueenMoves(move.endRank, move.endFile, moves)
        else:
            moves = []

        if self.check(moves):
            return True
        return False

    def findLegalMoves(self):
        return self.generateMoves(self.findPieceLegalMoves())

    # --- Sliding Pieces --- #
    def getBishopMoves(self, rank, file, moves):
        """
        Need to check each direction, one square at a time, extending away from the piece, stopping when it hits a piece
        """
        diagonal_directions = [
            (-1, 1),  # Up and Right
            (1, 1),  # Down and Right
            (1, -1),  # Down and Left
            (-1, -1)  # Up and Left
        ]

        for direction in diagonal_directions:
            for i in range(1, 8):
                end_file = file + direction[1] * i
                end_rank = rank + direction[0] * i

                if 0 <= end_file < 8 and 0 <= end_rank < 8:  # If the bishop stays on the board
                    end_piece = self.virtualBoard[end_rank][end_file]

                    if end_piece == "0":  # Square is empty
                        moves.append(Move(rank, file, end_rank, end_file, self.virtualBoard))
                    elif end_piece[-1] != self.player:  # Square doesn't contain a friendly piece
                        moves.append(Move(rank, file, end_rank, end_file, self.virtualBoard))
                        break
                    else:
                        break
                else:
                    break

    def getRookMoves(self, rank, file, moves):
        """
        Need to check each direction, one square at a time, extending away from the piece, stopping when it hits a piece
        """
        orthogonal_directions = [
            (-1, 0),  # Up
            (1, 0),  # Down
            (0, -1),  # Left
            (0, 1)  # Right
        ]

        for direction in orthogonal_directions:
            for i in range(1, 8):
                end_file = file + direction[1] * i
                end_rank = rank + direction[0] * i

                if 0 <= end_file < 8 and 0 <= end_rank < 8:  # If the rook stays on the board
                    end_piece = self.virtualBoard[end_rank][end_file]

                    if end_piece == "0":  # Square is empty
                        moves.append(Move(rank, file, end_rank, end_file, self.virtualBoard))
                    elif end_piece[-1] != self.player:  # Square doesn't contain a friendly piece
                        moves.append(Move(rank, file, end_rank, end_file, self.virtualBoard))
                        break
                    else:  # Friendly piece, invalid
                        break
                else:  # Off board, invalid
                    break

    def getQueenMoves(self, rank, file, moves):
        """
        Moves like a rook and a bishop, so let's just reuse those methods.
        """
        self.getBishopMoves(rank, file, moves)
        self.getRookMoves(rank, file, moves)

    # --- Different Moving Pieces --- #
    def getPawnMoves(self, rank, file, moves):
        """
        Get all of the possible pawn moves, based on the pawn at the inputted rank and file, and then add those moves
        to the moves list
        """

        # --- White Pawns --- #
        if self.whiteToMove:
            if self.virtualBoard[rank - 1][file] == "0":  # Checks the square in front of the pawn is empty
                moves.append(Move(rank, file, rank - 1, file, self.virtualBoard))
                # Checks if a 2 square pawn move is possible
                if rank == 6 and self.virtualBoard[rank - 2][file] == "0":
                    moves.append(Move(rank, file, rank - 2, file, self.virtualBoard))

            # Adds the pawn captures to the legal moves list
            if file + 1 < 8:
                # Pawn captures right
                if self.virtualBoard[rank - 1][file + 1][-1] == "k":
                    moves.append(Move(rank, file, rank - 1, file + 1, self.virtualBoard))

            if file - 1 > -1:
                # Pawn captures left
                if self.virtualBoard[rank - 1][file - 1][-1] == "k":
                    moves.append(Move(rank, file, rank - 1, file - 1, self.virtualBoard))

        # --- Black Pawns --- #
        if not self.whiteToMove:
            if self.virtualBoard[rank + 1][file] == "0":  # Checks the square in front of the pawn is empty
                moves.append(Move(rank, file, rank + 1, file, self.virtualBoard))
                # Checks if a 2 square pawn move is possible
                if rank == 1 and self.virtualBoard[rank + 2][file] == "0":
                    moves.append(Move(rank, file, rank + 2, file, self.virtualBoard))
                    self.enPassantPossibleWhite = True

            # Adds the pawn captures to the legal moves list
            if file + 1 < 8:
                # Pawn captures right
                if self.virtualBoard[rank + 1][file + 1][-1] == "e":
                    moves.append(Move(rank, file, rank + 1, file + 1, self.virtualBoard))

            if file - 1 > -1:
                # Pawn captures left
                if self.virtualBoard[rank + 1][file - 1][-1] == "e":
                    moves.append(Move(rank, file, rank + 1, file - 1, self.virtualBoard))

    def getKnightMoves(self, rank, file, moves):
        knight_moves = [
            (2, 1),
            (1, 2),
            (-1, 2),
            (-2, 1),
            (-2, -1),
            (-1, -2),
            (1, -2),
            (2, -1)
        ]
        for move in knight_moves:
            end_rank = rank + move[0]
            end_file = file + move[1]

            if 0 <= end_rank < 8 and 0 <= end_file < 8:  # If the Knight stays on the board
                end_piece = self.virtualBoard[end_rank][end_file]
                if end_piece[-1] != self.player:  # Not the same colour piece
                    moves.append(Move(rank, file, end_rank, end_file, self.virtualBoard))

    def getKingMoves(self, rank, file, moves):
        king_moves = [
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
            (0, -1),
            (1, -1)
        ]
        for move in king_moves:
            endRank = rank + move[0]
            endFile = file + move[1]

            if 0 <= endRank <= 7 and 0 <= endFile <= 7:  # If the King stays on the board
                end_piece = self.virtualBoard[endRank][endFile]

                if end_piece[-1] != self.player:  # Not the same colour piece
                    moves.append(Move(rank, file, endRank, endFile, self.virtualBoard))

    def updateKings(self, move):
        """
        Add check logic here ??
        """
        if move.pieceMoved == "King_white":
            self.whiteKingCoords = (move.endRank, move.endFile)
        if move.pieceMoved == "King_black":
            self.blackKingCoords = (move.endRank, move.endFile)

    def boardFromFEN(self):
        piecesFromFEN = {
            "K": "King_white",
            "k": "King_black",

            "Q": "queen_white",
            "q": "queen_black",

            "R": "rook_white",
            "r": "rook_black",

            "B": "bishop_white",
            "b": "bishop_black",

            "N": "knight_white",
            "n": "knight_black",

            "P": "pawn_white",
            "p": "pawn_black"
        }
        virtualBoard = []

        tempRank = self.fenString.split("/")

        # --- Set Up Pieces --- #
        for i in range(8):
            rank = []
            for char in tempRank[i]:
                if char == " ":
                    break
                elif char.isdigit():
                    rank += ["0"] * int(char)
                else:
                    rank.append(piecesFromFEN[char])

                # Find Kings
                if char == "K":
                    self.whiteKingCoords = (i, len(rank) - 1)
                if char == "k":
                    self.blackKingCoords = (i, len(rank) - 1)

            virtualBoard.append(rank)

        # --- Update Stats --- #
        gameState = tempRank[-1].split(" ")

        # Turns
        if gameState[1] == "w":
            self.whiteToMove = True
        else:
            self.whiteToMove = False

        # Castling
        castlingRights = gameState[2]
        if castlingRights != "-":
            if "K" in castlingRights:
                self.whiteCastling["kingside"] = True
            if "Q" in castlingRights:
                self.whiteCastling["queenside"] = True
            if "k" in castlingRights:
                self.blackCastling["kingside"] = True
            if "q" in castlingRights:
                self.blackCastling["queenside"] = True
        else:
            pass

        # En Passant
        enPassant = gameState[3]
        if enPassant != "-":
            self.enPassantPossible = True
            self.enPassantCoords = enPassant
        else:
            pass

        return virtualBoard


# --- Move Class --- #
class Move:
    def __init__(self, startRank, startFile, endRank, endFile, virtualBoard):
        try:
            # Start and End Position of the Move
            self.startRank = startRank
            self.startFile = startFile
            self.endRank = endRank
            self.endFile = endFile

            # Piece Identifiers
            self.pieceMoved = virtualBoard[self.startRank][self.startFile]
            self.pieceCaptured = virtualBoard[self.endRank][self.endFile]
            self.moveId = self.startRank * 1 + self.startFile * 0.1 + self.endRank * 0.01 + self.endFile * 0.001
        except IndexError:
            print("Cannot move piece off of board.")


        # Special Moves
        self.pawnPromotion = False
        if (self.pieceMoved[-1] == "e" and self.pieceMoved[0] == "p" and self.endRank == 0) or \
                (self.pieceMoved[-1] == "k" and self.pieceMoved[0] == "p" and self.endRank == 7):
            self.pawnPromotion = True

        self.enPassant = False

        self.twoSquareAdvance = False
        if (self.pieceMoved[-1] == "e" and self.pieceMoved[0] == "p" and self.startRank - self.endRank == 2) or \
                (self.pieceMoved[-1] == "k" and self.pieceMoved[0] == "p" and self.endRank - self.startRank == 2):
            self.twoSquareAdvance = True

        # --- File Num to Letter for str --- #
        self.intToLetter = {
            0: "a",
            1: "b",
            2: "c",
            3: "d",
            4: "e",
            5: "f",
            6: "g",
            7: "h",
        }

    def __eq__(self, other):
        """
        Overloading equals method to compare move objects based on moveId
        :param other: other move object to compare
        :return: True if moveId is the same, False otherwise
        """
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False

    def __str__(self):
        """
        Overloading string method
        :return:
        """
        return f"{self.intToLetter[self.startFile]}{self.startRank}-{self.intToLetter[self.endFile]}{self.endRank}"
