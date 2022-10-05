# engine.py
class Engine:
    """
    Based on FEN requirements
    To Do: Half move clock
    - Since last capture or pawn move
    To Do: Full move number
    - Increments after blacks move
    """
    def __init__(self):
        # --- Board Representation --- #
        self.fenString = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        # --- Defaults --- #
        # --- Turns --- #
        self.whiteToMove = True
        if self.whiteToMove:
            self.player = "e"
        else:
            self.player = "k"

        # --- King State --- #
        self.whiteKingCoords = None
        self.blackKingCoords = None

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
                # if move.pieceMoved[-1] == "e":
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

    def generateMoves(self, psuedoLegalMoves):
        if len(self.moveLog) > 0:
            if self.moveLog[-1].twoSquareAdvance and self.whiteToMove:
                pass

                """
                # --- White Pawns --- #
                # En passant right
                if self.virtualBoard[rank][file + 1][-1] == "k" and self.enPassantPossibleWhite:
                    moves.append(Move(rank, file, rank - 1, file + 1, self.virtualBoard))
                    self.enPassantPossibleWhite = False    
                    
                # En passant left
                if self.virtualBoard[rank][file - 1][-1] == "k" and self.enPassantPossibleWhite:
                    moves.append(Move(rank, file, rank - 1, file - 1, self.virtualBoard))
                    self.enPassantPossibleWhite = False
                    
                # -- Black Pawns --- #
                # En passant right
                if self.virtualBoard[rank][file + 1][-1] == "e" and self.enPassantPossibleBlack:
                    moves.append(Move(rank, file, rank + 1, file + 1, self.virtualBoard))
                    self.enPassantPossibleBlack = False
                
                # En passant left
                if self.virtualBoard[rank][file - 1][-1] == "e" and self.enPassantPossibleBlack:
                    moves.append(Move(rank, file, rank + 1, file - 1, self.virtualBoard))
                    self.enPassantPossibleBlack = False
                """
        return psuedoLegalMoves

    def findPieceLegalMoves(self):
        legalMoves = []

        for file in range(len(self.virtualBoard)):
            for rank in range(len(self.virtualBoard)):
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

            if 0 <= endRank < 8 and 0 <= endFile < 8:  # If the King stays on the board
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
        # Start and End Position of the Move
        self.startRank = startRank
        self.startFile = startFile
        self.endRank = endRank
        self.endFile = endFile

        # Piece Identifiers
        self.pieceMoved = virtualBoard[self.startRank][self.startFile]
        self.pieceCaptured = virtualBoard[self.endRank][self.endFile]
        self.moveId = self.startRank * 1 + self.startFile * 0.1 + self.endRank * 0.01 + self.endFile * 0.001

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

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False
