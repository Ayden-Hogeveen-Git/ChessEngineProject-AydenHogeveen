# engine.py
class Engine:
    """
    TODO: Castling
    TODO: Checkmate
    TODO: En Passant

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
        """
        Makes a move on the board, updating the board state accordingly
        :param move: Move (move object to make)
        :return: None
        """
        if (move.startRank != move.endRank or move.startFile != move.endFile):
            # Basic Move Making
            self.virtualBoard[move.startRank][move.startFile] = "0"
            self.virtualBoard[move.endRank][move.endFile] = move.pieceMoved
            self.moveLog.append(move)

            # Handle castling
            if (move.isCastle):
                if (move.endFile == 6):  # Kingside castling
                    self.virtualBoard[move.endRank][5] = self.virtualBoard[move.endRank][7]
                    self.virtualBoard[move.endRank][7] = "0"
                else:  # Queenside castling
                    self.virtualBoard[move.endRank][3] = self.virtualBoard[move.endRank][0]
                    self.virtualBoard[move.endRank][0] = "0"

            # Switch Turns
            self.whiteToMove = not self.whiteToMove

            # Pawn Promotion
            if (move.pawnPromotion):
                if (self.whiteToMove):
                    self.virtualBoard[move.endRank][move.endFile] = "queen_black"
                else:
                    self.virtualBoard[move.endRank][move.endFile] = "queen_white"

            # En Passant
            if (move.enPassant):
                print("possible en passant")

            # King Moves
            self.updateKings(move)

            # Update castling rights
            self.updateCastlingRights(move)


    def takeback(self):
        """
        Takes back the previously taken move, and updates the board state accordingly, uses the move log to refer
        to previous moves
        :return: None
        """
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
        """
        Finds the moves that each piece can make according to the rules for each piece in isolation
        :return legalMoves: arr (list of moves the player could make)
        """
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
        1. Makes the move
        2. Checks if the king is in check
        3. If the king is in check, the move is illegal, don't add it to the list
            else: add to legal moves
        4. Check next move
        :param psuedoLegal: arr (list of moves a player could make with the pieces, before accounting for the rules)
        :return legal: arr (list of moves a player can make in the position)
        """
        legal = []

        for move in psuedoLegal:
            self.makeMove(move)
            if (not self.inCheck()):
                legal.append(move)
            self.takeback()
        
        return legal

    def inCheck(self):
        """
        Determines if the king is in check in the current position
        :return: bool (True if king is in check, False otherwise)
        """
        if self.whiteToMove:
            return self.squareUnderAttack(self.blackKingCoords[0], self.blackKingCoords[1])
        else:
            return self.squareUnderAttack(self.whiteKingCoords[0], self.whiteKingCoords[1])
    
    def squareUnderAttack(self, rank, file):
        """
        Determines if a particular square is under attack
        :param rank: int (rank of the square)
        :param file: int (file of the square)
        :return: bool (True if square is under attack, False otherwise)
        """
        self.whiteToMove = not self.whiteToMove  # Switch to opponent's turn
        opponentMoves = self.findPieceLegalMoves()  # Find opponent's legal moves
        self.whiteToMove = not self.whiteToMove  # Switch back to original player's turn

        for move in opponentMoves:
            if move.endRank == rank and move.endFile == file:
                return True
        return False

    def findLegalMoves(self):
        """
        Returns legal moves in a position using above helper functions
        :return: arr (legal moves)
        """
        return self.generateMoves(self.findPieceLegalMoves())

    # --- Sliding Pieces --- #
    def getBishopMoves(self, rank, file, moves):
        """
        Need to check each direction, one square at a time, extending away from the piece, stopping when it hits a piece
        :param rank: int (rank of the chessboard)
        :param file: int (file on the chessboard)
        :param moves: arr (list of move objects the player could make in isolation)
        :return: None
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
        :param rank: int (rank of the chessboard)
        :param file: int (file on the chessboard)
        :param moves: arr (list of move objects the player could make in isolation)
        :return: None
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
        :param rank: int (rank of the chessboard)
        :param file: int (file on the chessboard)
        :param moves: arr (list of move objects the player could make in isolation)
        :return: None
        """
        self.getBishopMoves(rank, file, moves)
        self.getRookMoves(rank, file, moves)

    # --- Different Moving Pieces --- #
    def getPawnMoves(self, rank, file, moves):
        """
        Get all of the possible pawn moves, based on the pawn at the inputted rank and file, and then add those moves
        to the moves list
        :param rank: int (rank of the chessboard)
        :param file: int (file on the chessboard)
        :param moves: arr (list of move objects the player could make in isolation)
        :return: None
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
        """
        Finds all possible knight moves in the position.
        :param rank: int (rank of the chessboard)
        :param file: int (file on the chessboard)
        :param moves: arr (list of move objects the player could make in isolation)
        :return: None
        """
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
        """
        Finds all possible king moves for the position
        :param rank: int (rank of the chessboard)
        :param file: int (file on the chessboard)
        :param moves: arr (list of move objects the player could make in isolation)
        :return: None
        """
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

            if (0 <= endRank <= 7 and 0 <= endFile <= 7):  # If the King stays on the board
                end_piece = self.virtualBoard[endRank][endFile]

                if (end_piece[-1] != self.player):  # Not the same colour piece
                    moves.append(Move(rank, file, endRank, endFile, self.virtualBoard))

        # Castling
        if (self.whiteToMove):
            if (self.whiteCastling["kingside"] and self.virtualBoard[7][5] == "0" and self.virtualBoard[7][6] == "0" and not self.squareUnderAttack(7, 4) and not self.squareUnderAttack(7, 5) and not self.squareUnderAttack(7, 6)):
                moves.append(Move(rank, file, 7, 6, self.virtualBoard, isCastle=True))
            if (self.whiteCastling["queenside"] and self.virtualBoard[7][1] == "0" and self.virtualBoard[7][2] == "0" and self.virtualBoard[7][3] == "0" and not self.squareUnderAttack(7, 4) and not self.squareUnderAttack(7, 2) and not self.squareUnderAttack(7, 3)):
                moves.append(Move(rank, file, 7, 2, self.virtualBoard, isCastle=True))
        else:
            if (self.blackCastling["kingside"] and self.virtualBoard[0][5] == "0" and self.virtualBoard[0][6] == "0" and not self.squareUnderAttack(0, 4) and not self.squareUnderAttack(0, 5) and not self.squareUnderAttack(0, 6)):
                moves.append(Move(rank, file, 0, 6, self.virtualBoard, isCastle=True))
            if (self.blackCastling["queenside"] and self.virtualBoard[0][1] == "0" and self.virtualBoard[0][2] == "0" and self.virtualBoard[0][3] == "0" and not self.squareUnderAttack(0, 4) and not self.squareUnderAttack(0, 2) and not self.squareUnderAttack(0, 3)):
                moves.append(Move(rank, file, 0, 2, self.virtualBoard, isCastle=True))
        


    def updateKings(self, move):
        """
        Updates the position of the Kings every move (inefficient, but it works)
        """
        for rank in range(8):
            for file in range(8):
                if self.virtualBoard[rank][file] == "King_white":
                    self.whiteKingCoords = (rank, file)
                if self.virtualBoard[rank][file] == "King_black":
                    self.blackKingCoords = (rank, file)

    def updateCastlingRights(self, move):
        """
        Method to track the castling rights of each player, specifically the movement of the Kings and Rooks
        :param move: Move (move object to make)
        :return: None
        """
        if (move.pieceMoved == "King_white"):
            self.whiteCastling["kingside"] = False
            self.whiteCastling["queenside"] = False
            print("king moved")
        elif (move.pieceMoved == "King_black"):
            self.blackCastling["kingside"] = False
            self.blackCastling["queenside"] = False
            print("king moved")

        elif (move.pieceMoved == "rook_white"):
            if (move.startRank == 7):
                if (move.startFile == 0):
                    self.whiteCastling["queenside"] = False
                    print("rook moved")

                elif (move.startFile == 7):
                    self.whiteCastling["kingside"] = False
                    print("rook moved")

        elif (move.pieceMoved == "rook_black"):
            if (move.startRank == 0):
                if (move.startFile == 0):
                    self.blackCastling["queenside"] = False
                    print("rook moved")

                elif (move.startFile == 7):
                    self.blackCastling["kingside"] = False
                    print("rook moved")



    def boardFromFEN(self):
        """
        Function to create a virtual board based on a Forsyth Edwards Notation (or FEN) string representation.
        :return virtualBoard: arr (2D array representation of a chessboard)
        """
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
                if (char == " "):
                    break
                elif (char.isdigit()):
                    rank += ["0"] * int(char)
                else:
                    rank.append(piecesFromFEN[char])

                # Find Kings
                if (char == "K"):
                    self.whiteKingCoords = (i, len(rank) - 1)
                if (char == "k"):
                    self.blackKingCoords = (i, len(rank) - 1)

            virtualBoard.append(rank)

        # --- Update Stats --- #
        gameState = tempRank[-1].split(" ")

        # Turns
        if (gameState[1] == "w"):
            self.whiteToMove = True
        else:
            self.whiteToMove = False

        # Castling
        castlingRights = gameState[2]
        if (castlingRights != "-"):
            if ("K" in castlingRights):
                self.whiteCastling["kingside"] = True
            if ("Q" in castlingRights):
                self.whiteCastling["queenside"] = True
            if ("k" in castlingRights):
                self.blackCastling["kingside"] = True
            if ("q" in castlingRights):
                self.blackCastling["queenside"] = True
        else:
            pass

        # En Passant
        enPassant = gameState[3]
        if (enPassant != "-"):
            self.enPassantPossible = True
            self.enPassantCoords = enPassant
        else:
            pass

        return virtualBoard


# --- Move Class --- #
class Move:
    def __init__(self, startRank, startFile, endRank, endFile, virtualBoard, isCastle=False):
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
        except (IndexError):
            print("Cannot move piece off of board.")

        # Special Moves
        self.pawnPromotion = False
        if (self.pieceMoved[-1] == "e" and self.pieceMoved[0] == "p" and self.endRank == 0) or \
                (self.pieceMoved[-1] == "k" and self.pieceMoved[0] == "p" and self.endRank == 7):
            self.pawnPromotion = True

        self.enPassant = False
        self.isCastle = isCastle

        self.twoSquareAdvance = False
        if (self.pieceMoved[-1] == "e" and self.pieceMoved[0] == "p" and self.startRank - self.endRank == 2) or \
                (self.pieceMoved[-1] == "k" and self.pieceMoved[0] == "p" and self.endRank - self.startRank == 2):
            self.twoSquareAdvance = True

        # --- Piece/File/Rank Adjustment for Notation --- #
        self.pieceCast = {
            "0": "",
            "p": "",
            "k": "N",
            "b": "B",
            "r": "R",
            "q": "Q",
            "K": "K"
        }
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
        if (isinstance(other, Move)):
            return self.moveId == other.moveId
        return False

    def __str__(self):
        """
        Overloading string method
        :return: str (string representation of a chess move)
        """
        if (self.isCastle):
            if (self.endFile == 6):
                return "O-O"
            else:
                return "O-O-O"
        if (self.pieceCaptured != "0"):
            if (self.pieceMoved[0] == "p"):
                return f"{self.intToLetter[self.startFile]}x{self.intToLetter[self.endFile]}{8 - self.endRank}"
            else:
                return f"{self.pieceCast[self.pieceMoved[0]]}x{self.intToLetter[self.endFile]}{8 - self.endRank}"
        return f"{self.pieceCast[self.pieceMoved[0]]}{self.intToLetter[self.endFile]}{8 - self.endRank}"
