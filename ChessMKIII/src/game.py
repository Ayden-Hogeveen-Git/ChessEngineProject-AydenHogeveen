# game.py
from board import Board, Colour
from engine import Engine, Move
import pygame

pygame.init()

# --- Screen Variables --- #
w, h = 800, 800
caption = "Chess"
fps = 60

screen = pygame.display.set_mode((w, h))
pygame.display.set_caption(caption)
pygame.display.set_icon(pygame.image.load("assets/CHESSICON.png"))

clock = pygame.time.Clock()


# --- Main Game Class --- #
class Game:
    def __init__(self):
        self.running = True

        # --- ChessBoard --- #
        self.board = Board(screen)
        self.fileTranslations = {
            0: "a",
            1: "b",
            2: "c",
            3: "d",
            4: "e",
            5: "f",
            6: "g",
            7: "h"
        }
        self.rankTranslations = {
            0: 8,
            1: 7,
            2: 6,
            3: 5,
            4: 4,
            5: 3,
            6: 2,
            7: 1
        }
        self.pieceOffset = w // 16

        # --- Player --- #
        self.holding = False
        self.heldPiece = None

        # --- Board Representation and Logic --- #
        self.engine = Engine()

        # --- Move Conditions --- #
        self.legalMoves = self.engine.findLegalMoves()
        self.moveMade = False  # Flags a move is made, so we can perform expensive operations

        # --- Game Conditions --- #
        self.whitePlayer = True
        self.blackPlayer = False
        self.whiteInCheck = False
        self.blackInCheck = False

        self.GAME_OVER = False

    def highlightLegalMoves(self, rank, file):
        # Transparent Square
        # surface = pygame.Surface((self.board.square_size, self.board.square_size))
        # surface.set_alpha(100)  # Transparency value 0 --> High, 255 --> None
        # surface.fill(Colour.GREY)
        # screen.blit(surface, (file * self.board.square_size, rank * self.board.square_size))

        pygame.draw.rect(screen, Colour.DARK_GREY, (file * self.board.squareSize, rank * self.board.squareSize,
                                                    self.board.squareSize, self.board.squareSize), w // 256)

        # Circles
        # Highlight Moves
        for move in self.legalMoves:
            if move.start_file == file and move.start_rank == rank:
                pygame.draw.circle(screen, Colour.HIGHLIGHT_COLOUR,
                                   (move.end_file * self.board.squareSize + self.board.squareSize / 2,
                                    move.end_rank * self.board.squareSize + self.board.squareSize / 2),
                                   self.board.squareSize / 6)

    def run(self):
        # --- Gameplay Loop --- #
        screen.fill(Colour.GREY)

        while self.running:
            self.board.drawGame(self.engine.virtualBoard)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()

                    startRank = mousePos[1] // self.board.squareSize
                    startFile = mousePos[0] // self.board.squareSize

                    self.holding = True

                    self.heldPiece = self.engine.virtualBoard[startRank][startFile]
                    # self.engine.virtualBoard[startRank][startFile] = "0"

                if event.type == pygame.MOUSEBUTTONUP:
                    self.holding = False

                    mousePos = pygame.mouse.get_pos()

                    endRank = mousePos[1] // self.board.squareSize
                    endFile = mousePos[0] // self.board.squareSize

                    currentMove = Move(startRank, startFile, endRank, endFile, self.engine.virtualBoard)

                    if self.whiteInCheck or self.blackInCheck:
                        print(f"{self.fileTranslations[endFile]}{self.rankTranslations[endRank]}+")
                    else:
                        print(f"{self.fileTranslations[endFile]}{self.rankTranslations[endRank]}")

                    if True:  # currentMove in self.legalMoves:
                        if self.engine.whiteToMove:
                            pass
                        elif not self.engine.whiteToMove:
                            pass
                        else:
                            pass

                        self.engine.makeMove(currentMove)
                        self.moveMade = True

                    self.heldPiece = None

            if self.holding:
                mousePos = pygame.mouse.get_pos()
                screen.blit(self.board.images[self.heldPiece], pygame.Rect(mousePos[0] - self.pieceOffset,
                            mousePos[1] - self.pieceOffset, self.board.squareSize, self.board.squareSize))
                self.highlightLegalMoves(startRank, startFile)

            if self.moveMade:
                # Check for legal moves
                self.legalMoves = None
                self.moveMade = False

            pygame.display.update()
        pygame.quit()
        clock.tick(fps)
