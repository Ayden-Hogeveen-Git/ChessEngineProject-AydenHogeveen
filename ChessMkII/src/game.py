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
clock = pygame.time.Clock()
fps = 60

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


# Main Class
class Main:
    """
    This class will be responsible for putting all of the other classes together, making the game run smoothly, and
    for running the game
    """

    def __init__(self):
        # Run Conditions
        self.running = True

        # Instantiations
        self.board = Board()
        self.engine = Engine()

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
        self.button_x = width * 81 // 100
        self.reset_button = Button(self.button_x, height * 4 / 10, width / 8, height / 16, Colour.WHITE, Colour.GREY,
                                   "Reset Board")
        self.takeback_button = Button(self.button_x, height * 6 / 10, width / 8, height / 16, Colour.WHITE, Colour.GREY,
                                      "Takeback")

        # Clocks
        self.starting_time = 180

        self.white_time = self.starting_time
        self.black_time = self.starting_time

        self.white_clock_on = False
        self.black_clock_on = False

        self.white_time_text = font.render(str(self.white_time), True, Colour.BLACK)
        self.black_time_text = font.render(str(self.black_time), True, Colour.BLACK)

        self.timer_border_width = width // 330

    def highlight_legal_moves(self, highlight_square):
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
                    pygame.draw.circle(screen, self.board.highlight_colour,
                                       (move.end_file * self.board.square_size + self.board.square_size / 2,
                                        move.end_rank * self.board.square_size + self.board.square_size / 2),
                                       self.board.square_size / 6)

    def drawUI(self):
        self.highlight_legal_moves(self.square_selected)

        self.reset_button.drawButton()
        self.takeback_button.drawButton()

        white_time_text = font.render(str(int(self.white_time)), True, (0, 0, 0))
        black_time_text = font.render(str(int(self.black_time)), True, (0, 0, 0))

        pygame.draw.rect(screen, Colour.WHITE, (self.button_x, height // 32, width // 8, height // 16))
        pygame.draw.rect(screen, Colour.GREY, (self.button_x, height // 32, width // 8, height // 16),
                         self.timer_border_width)

        pygame.draw.rect(screen, Colour.WHITE, (self.button_x, height * 29 // 32, width // 8, height // 16))
        pygame.draw.rect(screen, Colour.GREY, (self.button_x, height * 29 // 32, width // 8, height // 16),
                         self.timer_border_width)

        screen.blit(white_time_text, (self.button_x + width / 64, height / 32 + self.timer_border_width * 4))
        screen.blit(black_time_text, (self.button_x + width / 64, height * 29 / 32 + self.timer_border_width * 4))

    def run(self):
        # Setting the background colour
        screen.fill(Colour.WHITE)

        self.board.loadImages()

        while self.running:
            self.board.drawGame(self.engine.virtual_board)

            if self.white_clock_on:
                self.white_time -= 1 / fps
            elif self.black_clock_on:
                self.black_time -= 1 / fps

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

                # Mouse Events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.game_over and Is_Turn:
                        # Tracking the mouse's position
                        mouse_pos = pygame.mouse.get_pos()

                        # Refers to the X position of the mouse, in terms of squares
                        mouse_rank = mouse_pos[0] // self.board.square_size
                        # Refers to the Y position of the mouse, in terms of squares
                        mouse_file = mouse_pos[1] // self.board.square_size

                        if self.reset_button.mouseOn(mouse_pos):
                            self.engine = Engine()
                            self.legal_moves = self.engine.findLegalMoves()
                            self.square_selected = ()
                            self.player_clicked = []
                            self.move_made = False

                            self.white_time = self.starting_time
                            self.black_time = self.starting_time

                            self.white_clock_on = False
                            self.black_clock_on = False

                        if self.takeback_button.mouseOn(mouse_pos):
                            self.engine.takeback()
                            self.move_made = True

                        if mouse_pos[0] <= 720:
                            if self.square_selected == (mouse_rank, mouse_file):  # The player clicks the same square again
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
                                    if self.engine.white_to_move:
                                        self.white_clock_on = True
                                        self.black_clock_on = False
                                    elif not self.engine.white_to_move:
                                        self.white_clock_on = False
                                        self.black_clock_on = True
                                    else:
                                        self.white_clock_on = False
                                        self.black_clock_on = False

                                    self.engine.move(player_move)
                                    self.move_made = True

                                self.square_selected = ()
                                self.player_clicked = []

                if event.type == pygame.MOUSEBUTTONUP:
                    self.reset_button.colour1 = Colour.WHITE
                    self.reset_button.border_width = width // 330
                    self.takeback_button.colour1 = Colour.WHITE
                    self.takeback_button.border_width = width // 330

            if self.move_made:
                self.legal_moves = self.engine.findLegalMoves()
                self.move_made = False

            # Updates the Screen
            pygame.display.update()
            clock.tick(fps)


if __name__ == "__main__":
    main = Main()
    main.run()
    pygame.quit()
    quit()
