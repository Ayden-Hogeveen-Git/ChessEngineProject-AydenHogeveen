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
        self.enPassantPossible = False
        self.enPassantCoords = None

        # --- Game Conditions --- #
        self.isMate = False
        self.isStalemate = False

        # --- Set Up Board --- #
        self.virtualBoard = self.boardFromFEN()

        # --- Move Tracker --- #
        self.moveLog = []

    def makeMove(self, move):
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

        # King King Moves
        self.updateKings(move)

    def generateMoves(self):
        pass

    def findLegalMoves(self):
        legalMoves = []

        for file in range(len(self.virtualBoard)):
            for rank in range(len(self.virtualBoard)):
                self.player = self.virtualBoard[rank][file][-1]

                # White ends in an e, black in a k
                if self.player == "e" and self.whiteToMove or self.player == "k" and not self.whiteToMove:
                    piece_type = self.virtualBoard[rank][file][0]  # p-pawn, k-knight, b-bishop, r-rook, q-queen, K-king

                    if piece_type == "p":
                        self.getPawnMoves(rank, file, legalMoves)
                    elif piece_type == "k":
                        self.getKnightMoves(rank, file, legalMoves)
                    elif piece_type == "b":
                        self.getBiBopMoves(rank, file, legalMoves)
                    elif piece_type == "r":
                        self.getRookMoves(rank, file, legalMoves)
                    elif piece_type == "q":
                        self.getQueenMoves(rank, file, legalMoves)
                    elif piece_type == "K":
                        self.getKingMoves(rank, file, legalMoves)

        return legalMoves

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

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False
