# Example file showing a basic pygame "game loop"
import pygame
from utils.utils import *
GAME_STATE = "GAME"

# initialize pygame
pygame.init()
clock = pygame.time.Clock()
running = True

# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # check if the user pressed a key
        if event.type == pygame.KEYDOWN:
            # check if the user pressed space
            if event.key == pygame.K_SPACE:
                spawn_bullet()

    if GAME_STATE == "GAME": 
        # draw the screen
        draw_screen()
        # handle player movement
        handle_movement()
        # handle bullets
        if handle_bullets():
            GAME_STATE = "GAME_OVER"
  
    if GAME_STATE == "GAME_OVER":
        if draw_game_over():
            GAME_STATE = "GAME"

    # render the screen
    pygame.display.flip()
    # limit FPS to 60
    update_dt(clock.tick(60) / 1000)

pygame.quit()