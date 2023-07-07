# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

def check_boundary(pos):
    if pos.x < 0:
        pos.x = 0
    elif pos.x > screen.get_width():
        pos.x = screen.get_width()
    if pos.y < 0:
        pos.y = 0
    elif pos.y > screen.get_height():
        pos.y = screen.get_height()


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#443554")

    pygame.draw.circle(screen, "#19151c", player_pos, 4)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w or pygame.K_UP]:
        if keys[pygame.K_LSHIFT]:
            player_pos.y -= 600 * dt
        player_pos.y -= 300 * dt
    if keys[pygame.K_s or pygame.K_DOWN]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a or pygame.K_LEFT]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d or pygame.K_RIGHT]:
        player_pos.x += 300 * dt

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000 # limits FPS to 60

pygame.quit()