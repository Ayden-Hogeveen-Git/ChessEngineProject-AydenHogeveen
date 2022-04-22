# board.py
import pygame


# --- Colour Class --- #
class Colour:
    WHITE = (255, 255, 255)
    GREY = (45, 45, 45)
    BLACK = (0, 0, 0)

    # Brown Theme
    BROWN = (181, 136, 98)
    LIGHT_BROWN = (240, 217, 181)

    # Board Square Square Colours
    LIGHT_SQUARE = LIGHT_BROWN
    DARK_SQUARE = BROWN


# --- Board Class --- #
class Board:
    def __init__(self, screen):
        # Board Dimensions
        self.dimension = 8
        self.screen = screen
        self.w = self.h = screen.get_height()

        self.square_size = self.w // self.dimension

        # Colours
        self.colour1 = Colour.LIGHT_SQUARE
        self.colour2 = Colour.DARK_SQUARE
        self.board_colours = (self.colour1, self.colour2)

        # Images
        self.images = {}

        # Gamestate
        self.gamestate = []

    def createBoard(self):
        for rank in range(self.dimension):
            for file in range(self.dimension):
                squareColours = self.board_colours[((rank + file) % 2)]

                pygame.draw.rect(self.screen, squareColours,
                                 (rank * self.square_size, file * self.square_size, self.square_size,
                                  self.square_size))

    def loadImages(self):
        pieces = ["pawn_white", "rook_white", "knight_white", "bishop_white", "queen_white", "King_white",
                  "pawn_black", "rook_black", "knight_black", "bishop_black", "queen_black", "King_black"]
        for piece in pieces:
            self.images[piece] = pygame.transform.scale(pygame.image.load("assets/ChessPieces/" + piece + ".png"),
                                                        (self.square_size, self.square_size))

    def drawPieces(self, virtual_board):
        for x in range(self.dimension):
            for y in range(self.dimension):
                piece = virtual_board[y][x]
                if piece != "0":
                    self.screen.blit(self.images[piece], pygame.Rect(x * self.square_size, y * self.square_size,
                                                                     self.square_size, self.square_size))

    def drawGame(self, virtual_board):
        self.loadImages()
        self.createBoard()
        self.drawPieces(virtual_board)
        pieces = ["pawn_white", "rook_white", "knight_white", "bishop_white", "queen_white", "King_white",
                  "pawn_black", "rook_black", "knight_black", "bishop_black", "queen_black", "King_black"]
        for piece in pieces:
            self.images[piece] = pygame.transform.scale(
                pygame.image.load("assets/ChessPieces/" + piece + ".png"),
                (self.square_size, self.square_size))
