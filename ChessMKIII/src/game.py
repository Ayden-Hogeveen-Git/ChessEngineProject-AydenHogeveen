# game.py
from board import Board, Colour
from engine import Engine
import pygame

pygame.init()

# --- Screen Variables --- #
w, h = 800, 800
caption = "Chess"

screen = pygame.display.set_mode((w, h))
pygame.display.set_caption(caption)
pygame.display.set_icon(pygame.image.load("assets/CHESSICON.png"))


# --- Main Game Class --- #
class Game:
    def __init__(self):
        self.running = True
        self.holding = False

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

        # --- Board Representation and Logic --- #
        self.engine = Engine()

    def run(self):
        # --- Gameplay Loop --- #
        screen.fill(Colour.GREY)

        while self.running:
            self.board.drawGame(self.engine.virtual_board)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()

                    startRank = mousePos[1] // self.board.square_size
                    startFile = mousePos[0] // self.board.square_size

                    self.holding = True

                    held_piece = self.engine.virtual_board[startRank][startFile]
                    self.engine.virtual_board[startRank][startFile] = "0"

                if event.type == pygame.MOUSEBUTTONUP:
                    self.holding = False

                    mousePos = pygame.mouse.get_pos()

                    endRank = mousePos[1] // self.board.square_size
                    endFile = mousePos[0] // self.board.square_size

                    print(f"{self.fileTranslations[endFile]}{self.rankTranslations[endRank]}")

                    self.engine.virtual_board[endRank][endFile] = held_piece
                    held_piece = None

            if self.holding:
                mousePos = pygame.mouse.get_pos()
                screen.blit(self.board.images[held_piece], pygame.Rect(mousePos[0] - self.pieceOffset,
                            mousePos[1] - self.pieceOffset, self.board.square_size, self.board.square_size))

            pygame.display.update()
        pygame.quit()
