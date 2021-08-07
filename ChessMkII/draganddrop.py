# Requirement: First display a picture on the screen. When the mouse is pressed and moved, drag the picture to move with it. The mouse won’t move
import pygame


# Write a function to determine whether a point is within a certain range
# Point (x,y)
# Range rect(x,y,w,h)
def is_in_rect(pos, rect):
    x, y = pos
    rx, ry, rw, rh = rect
    if (rx <= x <= rx+rw) and (ry <= y <= ry+rh):
        return True
    return False


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    screen.fill((255, 255, 255))
    pygame.display.set_caption('Picture drag and drop')

    # Show a picture
    image = pygame.image.load('chessAssets/ChessPieces/queen_white.png')
    image_x = 100
    image_y = 100
    screen.blit(image, (image_x, image_y))
    pygame.display.flip()

    # Used to store whether the picture can be moved
    is_move = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            # Press the mouse to make the state become movable
            if event.type == pygame.MOUSEBUTTONDOWN:
                w, h = image.get_size()
                if is_in_rect(event.pos, (image_x, image_y, w, h)):
                    is_move = True

            # The mouse bounces up, so that the state cannot be moved
            if event.type == pygame.MOUSEBUTTONUP:
                is_move = False

            # Event corresponding to mouse movement
            if event.type == pygame.MOUSEMOTION:
                if is_move:
                    screen.fill((255, 255, 255))
                    x, y = event.pos
                    image_w, image_h = image.get_size()
                    # Ensure that the mouse is in the center of the picture
                    image_y = y-image_h/2
                    image_x = x-image_w/2
                    screen.blit(image, (image_x, image_y))
                    pygame.display.update()
