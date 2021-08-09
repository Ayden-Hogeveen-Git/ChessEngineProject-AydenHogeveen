# chess.py
"""
title: Chess MkII
author: Ayden Hogeveen
date-created: 2021-07-27
"""

import pygame

pygame.init()

# Creating the game window
width = height = 720
screen = pygame.display.set_mode((width, height))

# Background Sound


# Title and Icon
pygame.display.set_caption("Chess Game")
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


# Engine Class
class Engine:
    pass


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
        self.colour1 = self.colour.WHITE
        self.colour2 = self.colour.GREEN
        self.board_colours = (self.colour1, self.colour2)
        self.virtual_board = [
            ["rook_black", "knight_black", "bishop_black", "queen_black", "king_black", "bishop_black", "knight_black", "rook_black"],  # 8th Rank
            ["pawn_black", "pawn_black", "pawn_black", "pawn_black", "pawn_black", "pawn_black", "pawn_black", "pawn_black"],  # 7th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 6th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 5th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 4th Rank
            ["0", "0", "0", "0", "0", "0", "0", "0"],  # 3th Rank
            ["pawn_white", "pawn_white", "pawn_white", "pawn_white", "pawn_white", "pawn_white", "pawn_white", "pawn_white"],  # 2nd Rank
            ["rook_white", "knight_white", "bishop_white", "queen_white", "king_white", "bishop_white", "knight_white", "rook_white"]]  # 1st Rank
        """
        Notes about the virtual board:
        - Each piece is represented by a string, the string name is also the name of the .png file that holds the 
        image of the piece
        - A blank square is represented by a 0
        - To access a piece using the virtual board, use self.virtual_board[file][rank]
        """
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
        self.drag_drop = DragDrop()
        self.imgs = self.board.images
        self.square_selected = ()
        self.player_clicks = []
        self.clock = pygame.time.Clock()

    def run(self):
        global piece
        while self.running:
            # Setting the background colour
            screen.fill(Colour.BLACK)
            self.board.drawGame(self.board.virtual_board)

            pieces = ["pawn_white", "rook_white", "knight_white", "bishop_white", "queen_white", "king_white",
                      "pawn_black", "rook_black", "knight_black", "bishop_black", "queen_black", "king_black"]
            for piece in pieces:
                self.imgs[piece] = pygame.transform.scale(
                    pygame.image.load("chessAssets/ChessPieces/" + piece + ".png"),
                    (self.board.square_size, self.board.square_size))

            # Tracking the mouse's position
            mouse_pos = pygame.mouse.get_pos()

            mouse_rank = mouse_pos[0]//self.board.square_size
            mouse_file = mouse_pos[1]//self.board.square_size

            # Tracking events
            for event in pygame.event.get():
                # X Button
                if event.type == pygame.QUIT:
                    self.running = False

                # Mouse Events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Make the state 'held'
                    self.drag_drop.is_held = True
                    if self.drag_drop.is_held:
                        print("Holding a", self.board.virtual_board[mouse_file][mouse_rank], "at", mouse_rank, mouse_file)

                if event.type == pygame.MOUSEBUTTONUP:
                    # Make the state 'dropped'
                    self.drag_drop.is_held = False
                    if not self.drag_drop.is_held:
                        print("dropped at", mouse_rank, mouse_file)

                if event.type == pygame.MOUSEMOTION:
                    # Holding the piece while moving the mouse
                    if self.drag_drop.is_held:
                        piece_width = self.imgs[piece].get_width()
                        piece_height = self.imgs[piece].get_height()

            # Updates the Screen
            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.run()
