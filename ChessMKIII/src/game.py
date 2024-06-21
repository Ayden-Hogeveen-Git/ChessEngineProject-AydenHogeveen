# game.py
from board import Board, Colour
from engine import Engine, Move
from opponent import Opponent
import pygame

pygame.init()

# --- Screen Variables --- #
frame = True
w, h = 800, 800
caption = "Chess"
fps = 60

if frame:
    screen = pygame.display.set_mode((w, h))
else:
    screen = pygame.display.set_mode((w, h), pygame.NOFRAME)

pygame.display.set_caption(caption)
pygame.display.set_icon(pygame.image.load("ChessMKIII/src/assets/CHESSICON.png"))

clock = pygame.time.Clock()


# --- Main Game Class --- #
class Game:
    def __init__(self):
        self.running = True
        self.singlePlayer = True

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
        self.pieceOffset = w // (w // 50)

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

        self.opponent = Opponent()

    def highlightLegalMoves(self, rank, file):
        """
        Highlights legal moves for the currently held piece
        :param rank, file: location of the piece on the board
        :return: None
        """
        pygame.draw.rect(screen, Colour.DARK_GREY, ((file * self.board.squareSize),
                                                    (rank * self.board.squareSize),
                                                    self.board.squareSize, self.board.squareSize), w // 256)

        # Circles
        # Highlight Moves
        if (self.legalMoves):
            for move in self.legalMoves:
                if (move.startFile == file and move.startRank == rank):
                    pygame.draw.circle(screen, Colour.HIGHLIGHT_COLOUR,
                                       ((move.endFile * self.board.squareSize + self.board.squareSize / 2),
                                        (move.endRank * self.board.squareSize + self.board.squareSize / 2)),
                                       self.board.squareSize / 6)

    def highlightChecks(self, move):
        """
        Right now just highlights the kings
        TODO: add checks
        :param move: Move Object
        :return: None
        """

        surface = pygame.Surface((self.board.squareSize, self.board.squareSize))
        surface.set_alpha(100)  # Transparency value 0 --> High, 255 --> None
        surface.fill(Colour.HIGHLIGHT_CHECK)
        screen.blit(surface, (self.engine.blackKingCoords[1] * self.board.squareSize,
                                self.engine.blackKingCoords[0] * self.board.squareSize))
        
        surface = pygame.Surface((self.board.squareSize, self.board.squareSize))
        surface.set_alpha(100)  # Transparency value 0 --> High, 255 --> None
        surface.fill(Colour.HIGHLIGHT_CHECK)
        screen.blit(surface, (self.engine.whiteKingCoords[1] * self.board.squareSize,
                                self.engine.whiteKingCoords[0] * self.board.squareSize))

    def draw(self, startRank, startFile):
        """
        Draws the board
        :return: None
        """
        self.board.drawGame(self.engine.virtualBoard)

        if (self.holding and self.heldPiece != "0"):
                mousePos = pygame.mouse.get_pos()
                screen.blit(self.board.images[self.heldPiece], pygame.Rect(mousePos[0] - self.pieceOffset,
                                                                           mousePos[1] - self.pieceOffset,
                                                                           self.board.squareSize,
                                                                           self.board.squareSize))
                self.highlightLegalMoves(startRank, startFile)
                if (self.engine.moveLog):
                    self.highlightChecks(self.engine.moveLog[-1])

        pygame.display.update()
        clock.tick(fps)

    def run(self):
        """
        Main gameplay loop
        :return: None
        """
        startRank = startFile = -1

        while (self.running):
            self.draw(startRank, startFile)
                        
            humanTurn = (self.engine.whiteToMove and self.whitePlayer) or (not self.engine.whiteToMove and self.blackPlayer) if (self.singlePlayer) else True

            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    self.running = False
                if (event.type == pygame.KEYDOWN):
                    # --- Key Events --- #
                    if (event.key == pygame.K_ESCAPE):
                        self.running = False

                    if (event.key == pygame.K_LEFT):
                        self.engine.takeback()
                        self.moveMade = True

                    if (event.key == pygame.K_r):
                        for i in range(len(self.engine.moveLog)):
                            self.engine.takeback()
                            self.moveMade = True

                # --- Piece Movement --- #
                if (humanTurn):
                    if (event.type == pygame.MOUSEBUTTONDOWN):
                        mousePos = pygame.mouse.get_pos()

                        startRank = mousePos[1] // self.board.squareSize
                        startFile = mousePos[0] // self.board.squareSize

                        if (0 <= startFile <= 7 and 0 <= startRank <= 7):
                            self.holding = True

                            self.heldPiece = self.engine.virtualBoard[startRank][startFile]
                            # self.engine.virtualBoard[startRank][startFile] = "0"
                        else:
                            self.heldPiece = None

                    # --- Putting a piece down --- #
                    if (event.type == pygame.MOUSEBUTTONUP):
                        if (self.heldPiece):
                            self.holding = False

                            mousePos = pygame.mouse.get_pos()

                            endRank = mousePos[1] // self.board.squareSize
                            endFile = mousePos[0] // self.board.squareSize

                            if (0 <= endFile <= 7 and 0 <= endRank <= 7):
                                currentMove = Move(startRank, startFile, endRank, endFile, self.engine.virtualBoard)

                                if (currentMove in self.legalMoves):
                                    self.engine.makeMove(currentMove)
                                    self.moveMade = True

                                    if (self.whiteInCheck or self.blackInCheck):
                                        print(f"CHECK! {self.fileTranslations[endFile]}{self.rankTranslations[endRank]}+")
                                    else:
                                        if (not self.engine.whiteToMove):
                                            print(f"{(len(self.engine.moveLog) + 1) // 2}. {currentMove}", end=", ")
                                        else:
                                            print(f"{currentMove}")

                            self.heldPiece = None

                else:
                    computerMove = self.opponent.getMove(self.legalMoves)
                    if (computerMove):
                        self.engine.makeMove(computerMove)
                        self.moveMade = True
                    else:
                        print("checkmate")

            if (self.moveMade):
                # Check for legal moves
                self.legalMoves = self.engine.findLegalMoves()
                self.moveMade = False
                # print(f"White\nCoords: {self.engine.whiteKingCoords}\nBlack\nCoords: {self.engine.blackKingCoords}\n")
                # print(f"W: {self.engine.whiteCastling} B: {self.engine.blackCastling}\n")

        pygame.quit()
