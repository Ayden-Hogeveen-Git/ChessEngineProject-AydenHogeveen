# chess.py
"""
title: Chess MkII
author: Ayden Hogeveen
date-created: 2021-07-27
"""

import pygame
from engine import Engine, Move

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


# Colours Class
class Colour:
    # RGB Values

    WHITE = (230, 230, 230)
    BLACK = (0, 0, 0)

    GREY = (100, 100, 100)
    DARK_GREY = (50, 50, 50)

    RED = (200, 50, 25)

    GREEN = (0, 115, 65)

    BLUE = (0, 100, 175)

    LIGHT_BLUE = (100, 150, 185)

    LIGHT_BROWN = (255, 230, 190)
    BROWN = (190, 140, 105)

    DARK_BROWN = (125, 100, 75)

    PURPLE = (150, 0, 175)

    INDIGO = (75, 0, 100)

    WOOD = (100, 50, 0)

    DARK_GREEN = (0, 50, 0)


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


# Board Class
class Board:
    """
    This class will create the board, and be responsible for drawing the board and pieces
    """

    def __init__(self):
        self.dimension = 8  # 8x8 grid
        self.width = width
        self.height = height
        self.square_size = self.width // self.dimension
        self.colour = Colour()
        self.colour1 = self.colour.LIGHT_BROWN
        self.colour2 = self.colour.BROWN
        self.board_colours = (self.colour1, self.colour2)
        self.images = {}

    def drawBoard(self):
        for x in range(self.dimension):
            for y in range(self.dimension):
                squareColours = self.board_colours[((x + y) % 2)]
                pygame.draw.rect(screen, squareColours,
                                 (x * self.square_size, y * self.square_size, self.square_size, self.square_size))

    def loadImages(self):
        pieces = ["pawn_white", "rook_white", "knight_white", "bishop_white", "queen_white", "king_white", "pawn_black", "rook_black", "knight_black", "bishop_black", "queen_black", "king_black"]
        for piece in pieces:
            self.images[piece] = pygame.transform.scale(pygame.image.load("chessAssets/ChessPieces/" + piece + ".png"),
                                                        (self.square_size, self.square_size))

    def drawPieces(self, virtual_board):
        for x in range(self.dimension):
            for y in range(self.dimension):
                piece = virtual_board[y][x]
                if piece != "0":
                    screen.blit(self.images[piece], pygame.Rect(x * self.square_size, y * self.square_size, self.square_size, self.square_size))

    def drawGame(self, virtual_board):
        self.loadImages()
        self.drawBoard()
        self.drawPieces(virtual_board)
        pieces = ["pawn_white", "rook_white", "knight_white", "bishop_white", "queen_white", "king_white",
                  "pawn_black", "rook_black", "knight_black", "bishop_black", "queen_black", "king_black"]
        for piece in pieces:
            self.images[piece] = pygame.transform.scale(
                pygame.image.load("chessAssets/ChessPieces/" + piece + ".png"),
                (self.square_size, self.square_size))


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
        self.board = Board()
        self.engine = Engine()
        self.drag_drop = DragDrop()
        self.imgs = self.board.images
        self.square_selected = ()
        self.player_clicked = []
        self.clock = pygame.time.Clock()

    def run(self):
        move_made = False  # Flag for moves that are made

        # Setting the background colour
        screen.fill(Colour.BLACK)

        self.board.loadImages()

        while self.running:
            self.board.drawGame(self.engine.virtual_board)

            # Tracking events
            for event in pygame.event.get():

                # X Button
                if event.type == pygame.QUIT:
                    self.running = False

                # Mouse Events
                if event.type == pygame.MOUSEBUTTONDOWN:
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
                        move = Move(self.player_clicked[0], self.player_clicked[1], self.engine.virtual_board)
                        print(move.getChessNotation())

                        self.engine.move(move)
                        move_made = True
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

            # Updates the Screen
            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.run()
