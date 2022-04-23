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
        self.virtual_board = self.boardFromFEN()

        # --- Move Tracker --- #
        self.moveLog = []

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
        virtual_board = []

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

            virtual_board.append(rank)

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

        return virtual_board


