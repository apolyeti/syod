# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
running = True
dt = 0
BORDER_WIDTH = 20

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)



# also make sure to check if player is out of bounds
def check_bounds():
    bound_width = BORDER_WIDTH + 5
    if player_pos.x < bound_width:
        player_pos.x = bound_width
        return True
    if player_pos.x > screen.get_width() - bound_width:
        player_pos.x = screen.get_width() - bound_width
        return True
    if player_pos.y < bound_width:
        player_pos.y = bound_width
        return True
    if player_pos.y > screen.get_height() - bound_width:
        player_pos.y = screen.get_height() - bound_width
        return True
    return False

def handle_movement():
    if check_bounds():
        return
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w or pygame.K_UP]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s or pygame.K_DOWN]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a or pygame.K_LEFT]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d or pygame.K_RIGHT]:
        player_pos.x += 300 * dt

# game loop
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#443554")
    # create a border around the screen
    pygame.draw.rect(screen, "#19151c", (0, 0, screen.get_width(), screen.get_height()), BORDER_WIDTH)
    pygame.draw.circle(screen, "#19151c", player_pos, 4)

    handle_movement()

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000 # limits FPS to 60

pygame.quit()