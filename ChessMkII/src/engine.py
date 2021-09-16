# engine.py


class Engine:
    """
    Notes about the virtual board:
        - Each piece is represented by a string, the string name is also the name of the .png file that holds the
        image of the piece
        - A blank square is represented by a 0
        - To access a piece using the virtual board, use self.virtual_board[file][rank]

        - To access a piece --> rank, file
        - To assign a move --> file, rank
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
            ["rook_white", "knight_white", "bishop_white", "queen_white", "King_white", "bishop_white", "knight_white", "rook_white"]  # 1st Rank
            ]

        # Turns
        self.white_to_move = True
        if self.white_to_move:
            self.player = "e"
        else:
            self.player = "k"

        # Game Ending Conditions
        self.is_mate = False
        self.is_stalemate = False

        # Move Log
        self.move_log = []

    def move(self, move):
        # Basic Moves
        self.virtual_board[move.start_rank][move.start_file] = "0"
        self.virtual_board[move.end_rank][move.end_file] = move.piece_moved
        self.move_log.append(move)

        self.white_to_move = not self.white_to_move

        if move.pawn_promotion:
            if move.piece_moved[-1] == "e":
                self.virtual_board[move.end_rank][move.end_file] = "queen_white"
            else:
                self.virtual_board[move.end_rank][move.end_file] = "queen_black"

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

        If the king can be taken, move is not legal
        """
        # Temporary variables for this algorithm

        moves = self.findPseudoLegalMoves()

        return moves

    def findPseudoLegalMoves(self):
        # Moves inputted need to be in starting (rank, file), ending (rank, file) order
        moves = []
        for file in range(len(self.virtual_board)):
            for rank in range(len(self.virtual_board)):
                self.player = self.virtual_board[rank][file][-1]

                if self.player == "e" and self.white_to_move or self.player == "k" and not self.white_to_move:  # White ends in an e, black in a k
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
        """
        Need to check each direction, one square at a time, extending away from the piece, stopping when it hits a piece.
        """
        diagonal_directions = [
            (-1, 1),  # Up and Right
            (1, 1),   # Down and Right
            (1, -1),  # Down and Left
            (-1, -1)    # Up and Left
        ]

        for direction in diagonal_directions:
            for i in range(1, 8):
                end_file = file + direction[1] * i
                end_rank = rank + direction[0] * i

                if 0 <= end_file < 8 and 0 <= end_rank < 8:  # If the bishop stays on the board
                    end_piece = self.virtual_board[end_rank][end_file]

                    if end_piece == "0":  # Square is empty
                        moves.append(Move((file, rank), (end_file, end_rank), self.virtual_board))
                    elif end_piece[-1] != self.player:  # Square doesn't contain a friendly piece
                        moves.append(Move((file, rank), (end_file, end_rank), self.virtual_board))
                        break
                    else:
                        break
                else:
                    break

    def getRookMoves(self, rank, file, moves):
        """
        Need to check each direction, one square at a time, extending away from the piece, stopping when it hits a piece.
        """
        orthogonal_directions = [
            (-1, 0),  # Up
            (1, 0),   # Down
            (0, -1),  # Left
            (0, 1)    # Right
        ]

        for direction in orthogonal_directions:
            for i in range(1, 8):
                end_file = file + direction[1] * i
                end_rank = rank + direction[0] * i

                if 0 <= end_file < 8 and 0 <= end_rank < 8:  # If the rook stays on the board
                    end_piece = self.virtual_board[end_rank][end_file]

                    if end_piece == "0":  # Square is empty
                        moves.append(Move((file, rank), (end_file, end_rank), self.virtual_board))
                    elif end_piece[-1] != self.player:  # Square doesn't contain a friendly piece
                        moves.append(Move((file, rank), (end_file, end_rank), self.virtual_board))
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
        if self.white_to_move:
            if self.virtual_board[rank - 1][file] == "0":  # Checks the square in front of the pawn is empty
                moves.append(Move((file, rank), (file, rank - 1), self.virtual_board))
                if rank == 6 and self.virtual_board[rank - 2][file] == "0":  # Checks if a 2 square pawn move is possible
                    moves.append(Move((file, rank), (file, rank - 2), self.virtual_board))

            # Adds the pawn captures to the legal moves list
            if file + 1 < 8:
                # Pawn captures right
                if self.virtual_board[rank - 1][file + 1] != "0":
                    if self.virtual_board[rank - 1][file + 1][-1] == "k":
                        moves.append(Move((file, rank), (file + 1, rank - 1), self.virtual_board))

            if file - 1 > -1:
                # Pawn captures left
                if self.virtual_board[rank - 1][file - 1] != "0":
                    if self.virtual_board[rank - 1][file - 1][-1] == "k":
                        moves.append(Move((file, rank), (file - 1, rank - 1), self.virtual_board))

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
                    if self.virtual_board[rank + 1][file + 1][-1] == "e":
                        moves.append(Move((file, rank), (file + 1, rank + 1), self.virtual_board))
            if file - 1 > -1:
                # Pawn captures left
                if self.virtual_board[rank + 1][file - 1] != "0":
                    if self.virtual_board[rank + 1][file - 1][-1] == "e":
                        moves.append(Move((file, rank), (file - 1, rank + 1), self.virtual_board))

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
                end_piece = self.virtual_board[end_rank][end_file]
                if end_piece[-1] != self.player:  # Not the same colour piece
                    moves.append(Move((file, rank), (end_file, end_rank), self.virtual_board))

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
            end_rank = rank + move[0]
            end_file = file + move[1]

            if 0 <= end_rank < 8 and 0 <= end_file < 8:  # If the King stays on the board
                end_piece = self.virtual_board[end_rank][end_file]

                if end_piece[-1] != self.player:  # Not the same colour piece
                    moves.append(Move((file, rank), (end_file, end_rank), self.virtual_board))


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
        self.move_id = self.start_rank * 1 + self.start_file * 0.1 + self.end_rank * 0.01 + self.end_file * 0.001

        # Special Moves
        self.pawn_promotion = False

        if self.piece_moved[-1] == "e" and self.end_rank == 0 or self.piece_moved[-1] == "k" and self.end_rank == 7:
            self.pawn_promotion = True

        self.en_passant = False

        # Translations
        self.translate_ranks = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
        self.translated_ranks = {translate: key for key, translate in self.translate_ranks.items()}  # Reverses a Dictionary
        self.translate_files = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        self.translated_files = {translate: key for key, translate in self.translate_files.items()}  # Reverses a Dictionary

    def __eq__(self, other):
        """
        Overriding the equals method, so that our 2 identical moves (the one from the mouse,
        and the one in legal moves) are seen as equal, despite being different objects.

        Because we are using 2 instances of the same move action/piece movement, we need to make
        the program treat them as one
        """
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def getRankFile(self, file, rank):
        return str(self.translated_files[file] + self.translated_ranks[rank])

    def getChessNotation(self):
        
        return self.getRankFile(self.start_file, self.start_rank) + self.getRankFile(self.end_file, self.end_rank)
