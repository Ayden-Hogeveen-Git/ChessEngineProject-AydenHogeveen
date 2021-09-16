# chessClock.py
import pygame
pygame.init()

# Creating the game window
width, height = 240, 240
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 60

# Initializing Fonts
font = pygame.font.Font("/Users/Ayden/PycharmProjects/ChessEngineProject-AydenHogeveen/ChessMkII/chessAssets/LandasansMedium-ALJ6m.otf", 32)

white_time = 0
black_time = 0


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

        # Clocks
        self.white_time = 60
        self.black_time = 60

        self.white_clock_on = False
        self.black_clock_on = False

    def drawUI(self):
        white_time_text = font.render(str(int(self.white_time)), True, (0, 0, 0))
        black_time_text = font.render(str(int(self.black_time)), True, (0, 0, 0))

        pygame.draw.rect(screen, (255, 0, 0), (80, height // 4 - 10, 50, 50))
        pygame.draw.rect(screen, (255, 0, 0), (80, height // 2 - 10, 50, 50))

        screen.blit(white_time_text, (100, height / 4))
        screen.blit(black_time_text, (100, height / 2))

    def run(self):
        # Setting the background colour
        screen.fill((255, 255, 255))

        while self.running:
            if self.white_time > 0 and self.black_time > 0:
                if self.white_clock_on:
                    self.white_time -= 1 / fps
                elif self.black_clock_on:
                    self.black_time -= 1 / fps
            elif self.white_time == 0:
                print("Black wins")
            elif self.black_time == 0:
                print("White wins")

            self.drawUI()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.white_clock_on:
                        self.black_clock_on = True
                        self.white_clock_on = False
                    elif self.black_clock_on:
                        self.black_clock_on = False
                        self.white_clock_on = True
                    else:
                        self.white_clock_on = True

            # Updates the Screen
            pygame.display.update()
            clock.tick(fps)


if __name__ == "__main__":
    main = Main()
    main.run()
    pygame.quit()
    quit()
