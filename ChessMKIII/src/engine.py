# engine.py

class Engine:
    def __init__(self):
        # Board Representation
        self.virtual_board = [
            ["rook_black", "knight_black", "bishop_black", "queen_black", "King_black", "bishop_black", "knight_black",
             "rook_black"],  # 8th Rank
            ["pawn_black", "pawn_black", "pawn_black", "pawn_black", "pawn_black", "pawn_black", "pawn_black",
             "pawn_black"],  # 7th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 6th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 5th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 4th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 3th Rank
            ["pawn_white", "pawn_white", "pawn_white", "pawn_white", "pawn_white", "pawn_white", "pawn_white",
             "pawn_white"],  # 2nd Rank
            ["rook_white", "knight_white", "bishop_white", "queen_white", "King_white", "bishop_white", "knight_white",
             "rook_white"]  # 1st Rank
        ]

        # Turns
        self.white_to_move = True
        if self.white_to_move:
            self.player = "e"
        else:
            self.player = "k"

        # King State Variables
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)

        # Game Ending Conditions
        self.is_mate = False
        self.is_stalemate = False

        # Move Log
        self.move_log = []

"""
EXPERIMENTAL

class Piece:
    def __init__(self, team, name):
        self.team = team
        self.name = name
        self.string = self.team + self.name


class King(Piece):
    def __init__(self, team):
        super().__init__(team, "King")


class Queen(Piece):
    def __init__(self, team):
        super().__init__(team, "queen")


class Rook(Piece):
    def __init__(self, team):
        super().__init__(team, "rook")
        
        
class Bishop(Piece):
    def __init__(self, team):
        super().__init__(team, "bishop")
        

class Knight(Piece):
    def __init__(self, team):
        super().__init__(team, "knight")


class Pawn(Piece):
    def __init__(self, team):
        super().__init__(team, "pawn")


class Engine:
    def __init__(self):
        self.virtual_board = [
            [Rook("black"), Knight("black"), Bishop("black"), Queen("black"), King("black"), Bishop("black"), Knight("black"), Rook("black")],  # 8th Rank
            [Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black")],  # 7th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 6th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 5th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 4th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 3th Rank
            [Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white")],  # 2nd Rank
            [Rook("white"), Knight("white"), Bishop("white"), Queen("white"), King("white"), Bishop("white"), Knight("white"), Rook("white")],  # 1st Rank
        ]
"""
