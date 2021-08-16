# board.py
import pygame
from chess import width, height, screen


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


# Board Class
class Board:
    """
    This class will create the board, and be responsible for drawing the board and pieces
    """

    def __init__(self):
        # Dimensions
        self.dimension = 8
        self.width = width
        self.height = height
        self.square_size = self.width // self.dimension

        # Colours
        self.colour = Colour()
        self.colour1 = self.colour.WHITE
        self.colour2 = self.colour.GREEN
        self.board_colours = (self.colour1, self.colour2)

        # Images
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


