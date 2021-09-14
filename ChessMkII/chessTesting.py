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
width, height = 960, 720
screen = pygame.display.set_mode((width, height))

# Initializing Fonts
font = pygame.font.Font("chessAssets/LandasansMedium-ALJ6m.otf", 32)

# Background Sound


# Title and Icon
pygame.display.set_caption("Chess Testing Program")
icon = pygame.image.load("chessAssets/CHESSICON.png")
pygame.display.set_icon(icon)


# Button Class
class Button:
    def __init__(self, x, y, button_width, button_height, colour1, colour2, text=""):
        self.x = x
        self.y = y
        self.width = button_width
        self.height = button_height
        self.text = text
        self.colour1 = colour1
        self.colour2 = colour2
        self.border_width = width // 330

    def drawButton(self):
        pygame.draw.rect(screen, self.colour1, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.colour2, (self.x, self.y, self.width, self.height), self.border_width)

        text = font.render(self.text, True, Colour.BLACK)
        screen.blit(text, (self.x + self.width / 16, self.y + self.height / 4))

    def mouseOn(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]

        if self.x < mouse_x < self.x + self.width:
            if self.y < mouse_y < self.y + self.height:
                self.colour1 = Colour.LIGHT_GREY
                self.border_width = width // 200
                return True
        return False


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
        # Run Conditions
        self.running = True
        self.clock = pygame.time.Clock()

        # Instantiations
        self.board = Board()
        self.engine = Engine()
        self.drag_drop = DragDrop()

        # Images
        self.imgs = self.board.images

        # Player Clicks
        self.square_selected = ()
        self.player_clicked = []

        # Move Conditions
        self.legal_moves = self.engine.findLegalMoves()
        self.move_made = False  # Flags when a move is made, so we can perform expensive operations

        # Game Conditions
        self.white_isPlayer = True
        self.black_isPlayer = False
        self.game_over = False

        # Buttons
        self.reset_button = Button(width * 81 / 100, height / 32, width / 8, height / 16, Colour.WHITE, Colour.GREY,
                                   "Reset Board")
        self.takeback_button = Button(width * 81 / 100, height / 8, width / 8, height / 16, Colour.WHITE, Colour.GREY,
                                      "Takeback")

    def highlight_black_legal_moves(self, highlight_square):
        """
        Highlights the square selected and the moves possible for the piece on that square
        """
        if self.square_selected != ():
            file, rank = highlight_square
            # Square Selected is a piece that can be moved
            # Highlight the selected square
            # surface = pygame.Surface((self.board.square_size, self.board.square_size))
            # surface.set_alpha(100)  # Transparency value 0 --> High, 255 --> None
            # surface.fill(Colour.GREY)
            # screen.blit(surface, (file * self.board.square_size, rank * self.board.square_size))

            pygame.draw.rect(screen, Colour.DARK_GREY, (file * self.board.square_size, rank * self.board.square_size,
                                                        self.board.square_size, self.board.square_size), width // 256)

            # Highlight Moves
            for move in self.legal_moves:
                if move.start_file == file and move.start_rank == rank:
                    pygame.draw.circle(screen, Colour.GREY,
                                       (move.end_file * self.board.square_size + self.board.square_size / 2,
                                        move.end_rank * self.board.square_size + self.board.square_size / 2),
                                       self.board.square_size / 6)

    def drawUI(self):
        self.highlight_black_legal_moves(self.square_selected)

        self.reset_button.drawButton()
        self.takeback_button.drawButton()

    def run(self):
        # Setting the background colour
        screen.fill(Colour.WHITE)

        self.board.loadImages()

        while self.running:
            self.board.drawGame(self.engine.virtual_board)
            self.drawUI()

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

                    if event.key == pygame.K_r:
                        self.engine = Engine()
                        self.legal_moves = self.engine.findLegalMoves()
                        self.square_selected = ()
                        self.player_clicked = []
                        self.move_made = False

                # Mouse Events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.game_over and Is_Turn:

                        # Tracking the mouse's position
                        mouse_pos = pygame.mouse.get_pos()

                        mouse_rank = mouse_pos[
                                         0] // self.board.square_size  # Refers to the X position of the mouse, in terms of squares
                        mouse_file = mouse_pos[
                                         1] // self.board.square_size  # Refers to the Y position of the mouse, in terms of squares

                        # # Make the state 'held'
                        # self.drag_drop.is_held = True
                        # if self.drag_drop.is_held:
                        #     held_piece = engine.virtual_board[mouse_file][mouse_rank]
                        #     print("Holding a", held_piece, "at", mouse_rank, mouse_file)

                        if self.reset_button.mouseOn(mouse_pos):
                            self.engine = Engine()
                            self.legal_moves = self.engine.findLegalMoves()
                            self.square_selected = ()
                            self.player_clicked = []
                            self.move_made = False

                        if self.takeback_button.mouseOn(mouse_pos):
                            self.engine.takeback()
                            self.move_made = True

                        if mouse_pos[0] <= 720:
                            if self.square_selected == (
                            mouse_rank, mouse_file):  # The player clicks the same square again
                                # Reset, deselecting the piece
                                self.square_selected = ()
                                self.player_clicked = []
                            else:  # Player clicks a different square
                                self.square_selected = (mouse_rank, mouse_file)
                                self.player_clicked.append(self.square_selected)

                            if len(self.player_clicked) == 2:  # The player has clicked 2 different squares
                                # Move the piece on the first square to the second square
                                player_move = Move(self.player_clicked[0], self.player_clicked[1],
                                                   self.engine.virtual_board)
                                print(player_move.getChessNotation())

                                if player_move in self.legal_moves:
                                    self.engine.move(player_move)
                                    self.move_made = True
                                self.square_selected = ()
                                self.player_clicked = []

                if event.type == pygame.MOUSEBUTTONUP:
                    self.reset_button.colour1 = Colour.WHITE
                    self.reset_button.border_width = width // 330
                    self.takeback_button.colour1 = Colour.WHITE
                    self.takeback_button.border_width = width // 330

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
