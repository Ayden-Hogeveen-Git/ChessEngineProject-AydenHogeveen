# engine.py
"""
TODO:
Fix Pawn capture/fork bug
"""


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
            ["rook_black", "knight_black", "bishop_black", "queen_black", "King_black", "bishop_black", "knight_black", "rook_black"],  # 8th Rank
            ["pawn_black", "pawn_black", "pawn_black", "pawn_black", "pawn_black", "pawn_black", "pawn_black", "pawn_black"],  # 7th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 6th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 5th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 4th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 3th Rank
            ["pawn_white", "pawn_white", "pawn_white", "pawn_white", "pawn_white", "pawn_white", "pawn_white", "pawn_white"],  # 2nd Rank
            ["rook_white", "knight_white", "bishop_white", "queen_white", "King_white", "bishop_white", "knight_white", "rook_white"] # 1st Rank
            ]
        # Turns
        self.white_to_move = True

        # Game Ending Conditions
        self.is_mate = False
        self.is_stalemate = False

        # Special Move Conditions
        self.is_pawn_promotion = False  # Google En Passant
        self.is_en_passant = False

        # Move Log
        self.move_log = []

    def move(self, move):
        self.virtual_board[move.start_rank][move.start_file] = "0"
        self.virtual_board[move.end_rank][move.end_file] = move.piece_moved
        self.move_log.append(move)

        self.white_to_move = not self.white_to_move

    def takeback(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.virtual_board[move.start_rank][move.start_file] = move.piece_moved
            self.virtual_board[move.end_rank][move.end_file] = move.piece_captured

        self.white_to_move = not self.white_to_move

    def findLegalMoves(self):
        """
        Moves that are legally allowed in a game of chess, considering checks, pins

        Basic legal move generation algorithm
        1. Generate all of the possible moves
        2. For each move, make the move
        3. Generate all of the opponent's moves after that move
        4. If any of those moves attack or take the king, the candidate move is not valid
        """
        # Temporary variables for this algorithm

        moves = self.findPseudoLegalMoves()

        return moves

    def findPseudoLegalMoves(self):
        # Moves inputted need to be in starting (rank, file), ending (rank, file) order
        moves = []
        for file in range(len(self.virtual_board)):
            for rank in range(len(self.virtual_board)):
                player = self.virtual_board[rank][file][-1]

                if player == "e" and self.white_to_move or player == "k" and not self.white_to_move:  # White ends in an e, black in a k
                    piece_type = self.virtual_board[rank][file][0]  # p-pawn, k-knight, b-bishop, r-rook, q-queen, K-king

                    if piece_type == "p":
                        self.getPawnMoves(rank, file, moves)
                    elif piece_type == "k":
                        self.getKnightMoves(rank, file, moves)
                    elif piece_type == "b":
                        self.getBishopMoves(rank, file, moves)
                    elif piece_type == "r":
                        self.getRookMoves(rank, file, moves)
                    elif piece_type == "q":
                        self.getQueenMoves(rank, file, moves)
                    elif piece_type == "K":
                        self.getKingMoves(rank, file, moves)
        return moves

    # --- Sliding Pieces --- #
    def getBishopMoves(self, rank, file, moves):
        pass

    def getRookMoves(self, rank, file, moves):
        """
        Need to check all of the squares in the sub array, and all the squares with the same index in the entire array
        """

    def getQueenMoves(self, rank, file, moves):
        pass

    # --- Different Moving Pieces --- #
    def getPawnMoves(self, rank, file, moves):
        """
        Get all of the possible pawn moves, based on the pawn at the inputted rank and file, and then add those moves
        to the moves list
        """

        # --- White Pawns --- #
        if self.white_to_move:
            if self.virtual_board[rank - 1][file] == "0":  # Checks the square in front of the pawn is empty
                moves.append(Move((file, rank), (file, rank - 1), self.virtual_board))
                if rank == 6 and self.virtual_board[rank - 2][file] == "0":  # Checks if a 2 square pawn move is possible
                    moves.append(Move((file, rank), (file, rank - 2), self.virtual_board))

            # Adds the pawn captures to the legal moves list
            if file + 1 < 8:
                # Pawn captures right
                if self.virtual_board[rank - 1][file + 1] != "0":
                    moves.append(Move((file, rank), (file + 1, rank - 1), self.virtual_board))

            if file - 1 > -1:
                # Pawn captures left
                if self.virtual_board[rank - 1][file - 1] != "0":
                    moves.append(Move((file, rank), (file - 1, rank - 1), self.virtual_board))


            # Pawn Promotion

        # --- Black Pawns --- #
        if not self.white_to_move:
            if self.virtual_board[rank + 1][file] == "0":  # Checks the square in front of the pawn is empty
                moves.append(Move((file, rank), (file, rank + 1), self.virtual_board))
                if rank == 1 and self.virtual_board[rank + 2][file] == "0":  # Checks if a 2 square pawn move is possible
                    moves.append(Move((file, rank), (file, rank + 2), self.virtual_board))

            # Adds the pawn captures to the legal moves list
            # - Still need to add the protection against trying to move off the board
            if file + 1 < 8:
                # Pawn captures right
                if self.virtual_board[rank + 1][file + 1] != "0":
                    moves.append(Move((file, rank), (file + 1, rank + 1), self.virtual_board))
            if file - 1 > -1:
                # Pawn captures left
                if self.virtual_board[rank + 1][file - 1] != "0":
                    moves.append(Move((file, rank), (file - 1, rank + 1), self.virtual_board))

    def getKnightMoves(self, rank, file, moves):
        knight_moves = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2))
        if self.white_to_move:
            player = "w"
        else:
            player = "b"
        for move in knight_moves:
            end_rank = rank + move[0]
            end_file = file + move[1]
            if 0 <= end_rank < 8 and 0 <= end_file < 8:  # If the Knight stays on the board
                END_PIECE = self.virtual_board[end_rank][end_file]
                if END_PIECE[0] is not player:  # Not the same colour piece
                    moves.append(Move((file, rank), (end_file, end_rank), self.virtual_board))
        #
        # # --- White Knights --- #
        # if self.white_to_move:
        #     try:
        #         if self.virtual_board[rank - 1][file - 2] == "0" or self.virtual_board[rank - 1][file - 2][0] == "b":
        #             moves.append(Move((file, rank), (file - 2, rank - 1), self.virtual_board))
        #         if self.virtual_board[rank - 1][file + 2] == "0" or self.virtual_board[rank - 1][file - 2][0] == "b":
        #             moves.append(Move((file, rank), (file + 2, rank - 1), self.virtual_board))
        #         if self.virtual_board[rank + 1][file - 2] == "0" or self.virtual_board[rank - 1][file - 2][0] == "b":
        #             moves.append(Move((file, rank), (file - 2, rank + 1), self.virtual_board))
        #         if self.virtual_board[rank + 1][file + 2] == "0" or self.virtual_board[rank - 1][file - 2][0] == "b":
        #             moves.append(Move((file, rank), (file + 2, rank + 1), self.virtual_board))
        #         if self.virtual_board[rank - 2][file - 1] == "0" or self.virtual_board[rank - 1][file - 2][0] == "b":
        #             moves.append(Move((file, rank), (file - 1, rank - 2), self.virtual_board))
        #         if self.virtual_board[rank - 2][file + 1] == "0" or self.virtual_board[rank - 1][file - 2][0] == "b":
        #             moves.append(Move((file, rank), (file + 1, rank - 2), self.virtual_board))
        #         if self.virtual_board[rank + 2][file - 1] == "0" or self.virtual_board[rank - 1][file - 2][0] == "b":
        #             moves.append(Move((file, rank), (file - 1, rank + 2), self.virtual_board))
        #         if self.virtual_board[rank + 2][file + 1] == "0" or self.virtual_board[rank - 1][file - 2][0] == "b":
        #             moves.append(Move((file, rank), (file + 1, rank + 2), self.virtual_board))
        #     except IndexError:
        #         pass
        #
        # # --- Black Knights --- #
        # if not self.white_to_move:
        #     if self.virtual_board[rank + 1][file - 2] == "0" or self.virtual_board[rank + 1][file - 2][0] == "w":
        #         moves.append(Move((file, rank), (file - 2, rank + 1), self.virtual_board))

    def getKingMoves(self, rank, file, moves):
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
        self.move_id = self.start_rank * 0.1 + self.start_file * 0.01 + self.end_rank * 0.001 + self.end_file * 0.0001

        # Translations
        self.translate_ranks = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
        self.translated_ranks = {translate: key for key, translate in self.translate_ranks.items()}  # Reverses a Dictionary
        self.translate_files = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        self.translated_files = {translate: key for key, translate in self.translate_files.items()}  # Reverses a Dictionary

    def __eq__(self, other):
        """
        Overriding the equals method, so that our 2 identical moves (the one from the mouse,
        and the one in legal moves) are seen as equal, despite being different objects.
        """
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

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

