# engine.py

class Engine:
    """
    Notes about the virtual board:
        - Each piece is represented by a string, the string name is also the name of the .png file that holds the
        image of the piece
        - A blank square is represented by a 0
        - To access a piece using the virtual board, use self.virtual_board[file][rank]
    """
    def __init__(self):
        # Board Representation
        self.virtual_board = [
            ["rook_black", "knight_black", "bishop_black", "queen_black", "king_black", "bishop_black", "knight_black", "rook_black"],  # 8th Rank
            ["pawn_black", "pawn_black", "pawn_black", "pawn_black", "pawn_black", "pawn_black", "pawn_black", "pawn_black"],  # 7th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 6th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 5th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 4th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 3th Rank
            ["pawn_white", "pawn_white", "pawn_white", "pawn_white", "pawn_white", "pawn_white", "pawn_white", "pawn_white"],  # 2nd Rank
            ["rook_white", "knight_white", "bishop_white", "queen_white", "king_white", "bishop_white", "knight_white", "rook_white"] # 1st Rank
            ]
        # Turns
        self.white_to_move = True
        self.black_to_move = True

        # Game Ending Conditions
        self.is_mate = False
        self.is_stalemate = False

        # Special Move Conditions
        self.is_pawn_promotion = False  # Google En Passant
        self.is_en_passant = False

        # Piece Variables
        self.piece_type = "0"

        # Move Log
        self.move_log = []

    def move(self, move):
        self.virtual_board[move.start_rank][move.start_file] = "0"
        self.virtual_board[move.end_rank][move.end_file] = move.piece_moved
        self.move_log.append(move)

        # Piece Variables
        self.piece_type = self.virtual_board[move.start_rank][move.start_file]

        if self.white_to_move:
            self.white_to_move = False
        else:
            self.white_to_move = True

    def findLegalMoves(self, piece_type):
        pass


# Move Class
class Move:
    def __init__(self, start_square, end_square, virtual_board):
        # Start and End Position of the Move
        self.start_rank = start_square[1]
        self.start_file = start_square[0]
        self.end_rank = end_square[1]
        self.end_file = end_square[0]

        # Piece Identifiers
        self.piece_moved = virtual_board[self.start_rank][self.start_file]
        self.piece_captured = virtual_board[self.end_rank][self.end_file]
        self.move_id = self.start_rank * 10 + self.start_file * 1 + self.end_rank * 0.1 + self.end_file * 0.01

        # Translations
        self.translate_ranks = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
        self.translated_ranks = {translate: key for key, translate in self.translate_ranks.items()}  # Reverses a Dictionary
        self.translate_files = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        self.translated_files = {translate: key for key, translate in self.translate_files.items()}  # Reverses a Dictionary

    def getRankFile(self, file, rank):
        return str(self.translated_files[file] + self.translated_ranks[rank])

    def getChessNotation(self):
        # if self.piece_moved == "pawn_white" or "pawn_black":
        #     return self.getRankFile(self.end_file, self.end_rank)
        # elif self.piece_moved == "knight_white" or "knight_black":
        #     return "N" + self.getRankFile(self.end_file, self.end_rank)
        # elif self.piece_moved == "bishop_white" or "bishop_black":
        #     return "B" + self.getRankFile(self.end_file, self.end_rank)
        # elif self.piece_moved == "rook_white" or "rook_black":
        #     return "R" + self.getRankFile(self.end_file, self.end_rank)
        # elif self.piece_moved == "queen_white" or "queen_black":
        #     return "Q" + self.getRankFile(self.end_file, self.end_rank)
        # elif self.piece_moved == "king_white" or "knight_black":
        #     return "K" + self.getRankFile(self.end_file, self.end_rank)
        
        return self.getRankFile(self.start_file, self.start_rank) + self.getRankFile(self.end_file, self.end_rank)

