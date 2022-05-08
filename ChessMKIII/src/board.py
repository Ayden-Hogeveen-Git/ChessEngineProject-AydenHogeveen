# board.py
import pygame


# --- Colour Class --- #
class Colour:
    WHITE = (255, 255, 255)
    LIGHT_GREY = (100, 100, 100)
    GREY = (45, 45, 45)
    DARK_GREY = (25, 25, 25)
    BLACK = (0, 0, 0)

    # Brown Theme
    BROWN = (181, 136, 98)
    LIGHT_BROWN = (240, 217, 181)

    # Board Square Square Colours
    LIGHT_SQUARE = LIGHT_BROWN
    DARK_SQUARE = BROWN

    # Highlight Colour
    HIGHLIGHT_COLOUR = LIGHT_GREY


# --- Board Class --- #
class Board:
    def __init__(self, screen):
        # Board Dimensions
        self.dimension = 8
        self.screen = screen
        self.w = self.h = screen.get_height()

        self.squareSize = self.w // self.dimension

        # Colours
        self.colour1 = Colour.LIGHT_SQUARE
        self.colour2 = Colour.DARK_SQUARE
        self.boardColours = (self.colour1, self.colour2)

        # Images
        self.images = {}

        # Gamestate
        self.gamestate = []

    def createBoard(self):
        for rank in range(self.dimension):
            for file in range(self.dimension):
                squareColours = self.boardColours[((rank + file) % 2)]

                pygame.draw.rect(self.screen, squareColours,
                                 (rank * self.squareSize, file * self.squareSize, self.squareSize,
                                  self.squareSize))

    def loadImages(self):
        pieces = ["pawn_white", "rook_white", "knight_white", "bishop_white", "queen_white", "King_white",
                  "pawn_black", "rook_black", "knight_black", "bishop_black", "queen_black", "King_black"]
        for piece in pieces:
            self.images[piece] = pygame.transform.scale(pygame.image.load("assets/ChessPieces/" + piece + ".png"),
                                                        (self.squareSize, self.squareSize))

    def drawPieces(self, virtual_board):
        for rank in range(self.dimension):
            for file in range(self.dimension):
                piece = virtual_board[file][rank]
                if piece != "0":
                    self.screen.blit(self.images[piece], pygame.Rect(rank * self.squareSize, file * self.squareSize,
                                                                     self.squareSize, self.squareSize))

    def drawGame(self, virtual_board):
        self.loadImages()
        self.createBoard()
        self.drawPieces(virtual_board)
        pieces = ["pawn_white", "rook_white", "knight_white", "bishop_white", "queen_white", "King_white",
                  "pawn_black", "rook_black", "knight_black", "bishop_black", "queen_black", "King_black"]
        for piece in pieces:
            self.images[piece] = pygame.transform.scale(
                pygame.image.load("assets/ChessPieces/" + piece + ".png"),
                (self.squareSize, self.squareSize))
