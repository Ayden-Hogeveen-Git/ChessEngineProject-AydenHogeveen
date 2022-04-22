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

        # --- ChessBoard --- #
        self.board = Board(screen)
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

            pygame.display.update()
        pygame.quit()
