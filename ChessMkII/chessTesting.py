# game.py
"""
title: Chess MkII
author: Ayden Hogeveen
date-created: 2021-07-27
"""

import pygame
from engine import Engine, Move
from board import Board, Colour

pygame.init()
engine = Engine()

# Creating the game window
width = height = 720
screen = pygame.display.set_mode((width, height))

# Background Sound


# Title and Icon
pygame.display.set_caption("Chess Testing Program")
icon = pygame.image.load("chessAssets/CHESSICON.png")
pygame.display.set_icon(icon)


# Piece Master Class
class Piece:
    """
    This class will create the framework for all our piece classes, and will detail what every chess piece can do
    It will be inherited from by each individual piece and pawn
    """

    def __init__(self, rank, file, piece_type, team):
        self.rank = rank
        self.file = file
        self.piece_type = piece_type
        self.team = team


# Pawn Class
class Pawn(Piece):
    """
    This class refers to pawns, able to move forward(once or twice on their first move), take diagonally one square
    from themselves, take en-passant, and promote if able to reach the end of the board
    """

    def __init__(self, rank, file, piece_type, team):
        super().__init__(rank, file, piece_type, team)
        self.rank = rank
        self.file = file
        self.piece_type = "Pawn"
        self.team = team
        self.alive = True
        self.moved = False
        self.en_passant = False
        self.promoted = False
        if self.team == "white":
            self.piece_img = pygame.image.load("chessAssets/ChessPieces/pawn_white.png")
        else:
            self.piece_img = pygame.image.load("chessAssets/ChessPieces/pawn_black.png")


# Drag and Drop Class
class DragDrop:
    def __init__(self):
        self.is_held = False

    def holding_piece(self, rect, pos):
        rect_x, rect_y, rect_width, rect_height = rect

        player_x, player_y = pos

        if rect_y <= player_y <= rect_y + rect_height and rect_x <= player_x <= rect_x + rect_width:
            return True
        else:
            return False


# Main Class
class Main:
    """
    This class will be responsible for putting all of the other classes together, making the game run smoothly, and
    for running the game
    """

    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()

        self.board = Board()
        self.engine = Engine()
        self.drag_drop = DragDrop()

        self.imgs = self.board.images

        self.square_selected = ()
        self.player_clicked = []

        self.legal_moves = self.engine.findLegalMoves()
        self.legal_moves = [Move((4, 6), (4, 4), self.engine.virtual_board)]
        self.move_made = False  # Flags when a move is made, so we can perform expensive operations

        self.white_isPlayer = True
        self.black_isPlayer = False
        self.game_over = False

    def run(self):
        # Setting the background colour
        screen.fill(Colour.BLACK)

        self.board.loadImages()

        while self.running:
            self.board.drawGame(self.engine.virtual_board)

            Is_Turn = engine.white_to_move and self.white_isPlayer or not engine.white_to_move and self.black_isPlayer

            # Tracking events
            for event in pygame.event.get():

                # X Button
                if event.type == pygame.QUIT:
                    self.running = False

                # Key Events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    
                    if event.key == pygame.K_LEFT:
                        self.engine.takeback()
                        self.move_made = True

                # Mouse Events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.game_over and Is_Turn:
                        # Tracking the mouse's position
                        mouse_pos = pygame.mouse.get_pos()

                        mouse_rank = mouse_pos[0] // self.board.square_size  # Refers to the X position of the mouse, in terms of squares
                        mouse_file = mouse_pos[1] // self.board.square_size  # Refers to the Y position of the mouse, in terms of squares

                        # # Make the state 'held'
                        # self.drag_drop.is_held = True
                        # if self.drag_drop.is_held:
                        #     held_piece = engine.virtual_board[mouse_file][mouse_rank]
                        #     print("Holding a", held_piece, "at", mouse_rank, mouse_file)

                        if self.square_selected == (mouse_rank, mouse_file):  # The player clicks the same square again
                            # Reset, deselecting the piece
                            self.square_selected = ()
                            self.player_clicked = []
                        else:  # Player clicks a different square
                            self.square_selected = (mouse_rank, mouse_file)
                            self.player_clicked.append(self.square_selected)

                        if len(self.player_clicked) == 2:  # The player has clicked 2 different squares
                            # Move the piece on the first square to the second square
                            player_move = Move(self.player_clicked[0], self.player_clicked[1], self.engine.virtual_board)
                            print(player_move.getChessNotation())

                            if player_move in self.legal_moves:
                                self.engine.move(player_move)
                                self.move_made = True
                            self.square_selected = ()
                            self.player_clicked = []
                    
                # if event.type == pygame.MOUSEBUTTONUP:
                #     # Tracking the mouse's position
                #     mouse_pos = pygame.mouse.get_pos()
                #
                #     mouse_rank = mouse_pos[0] // self.board.square_size  # Refers to the X position of the mouse, in terms of squares
                #     mouse_file = mouse_pos[1] // self.board.square_size  # Refers to the Y position of the mouse, in terms of squares
                #
                #     # Make the state 'dropped'
                #     self.drag_drop.is_held = False
                #     if not self.drag_drop.is_held:
                #         print("dropped at", mouse_rank, mouse_file)

            if self.move_made:
                self.legal_moves = self.engine.findLegalMoves()
                self.move_made = False

            # Updates the Screen
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    main = Main()
    main.run()
