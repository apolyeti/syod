# Example file showing a basic pygame "game loop"
import pygame
from bullet import Bullet

# constants
SHOW_CONTROLS = True
BORDER_WIDTH = 20
PLAYER_RADIUS = 5
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TEXT_COLOR = "#bc7ad6"
BG_COLOR = "#443554"
BORDER_COLOR = "#19151c"

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# bullets
bullets = []
BULLET_SPEED = 300

def spawn_bullet():
    angle_step = 360 // 4
    for angle in range(0, 360, angle_step):
        bullet_dir = pygame.Vector2(1, 0).rotate(angle)
        bullet_pos = player_pos + bullet_dir * (PLAYER_RADIUS + 10)
        bullet = Bullet(bullet_pos, bullet_dir * BULLET_SPEED, 3)
        bullets.append(bullet)

def handle_bullets():
    for bullet in bullets:
        bullet.move(dt)
        if bullet.check_bounds(screen):
            bullet.bounce()
        if bullet.check_collision(player_pos):
            bullets.remove(bullet)




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

# check if player is holding shift
def check_sprint():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LSHIFT or pygame.K_RSHIFT]:
        return True
    return False

def handle_movement():
    global SHOW_CONTROLS
    if check_bounds():
        return
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w or pygame.K_UP]:
        if check_sprint():
            player_pos.y -= 500 * dt
        else: 
            player_pos.y -= 300 * dt
        SHOW_CONTROLS = False
    if keys[pygame.K_s or pygame.K_DOWN]:
        if check_sprint():
            player_pos.y += 500 * dt
        else:
            player_pos.y += 300 * dt
        SHOW_CONTROLS = False
    if keys[pygame.K_a or pygame.K_LEFT]:
        if check_sprint():
            player_pos.x -= 500 * dt
        else:
            player_pos.x -= 300 * dt
        SHOW_CONTROLS = False
    if keys[pygame.K_d or pygame.K_RIGHT]:
        if check_sprint():
            player_pos.x += 500 * dt
        else:
            player_pos.x += 300 * dt
        SHOW_CONTROLS = False










    
# draw the screen, border, and player
def draw_screen():
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, screen.get_width(), screen.get_height()), BORDER_WIDTH)
    pygame.draw.circle(screen, BORDER_COLOR, player_pos, PLAYER_RADIUS)

    for bullet in bullets:
        bullet.draw(screen)
    
    if SHOW_CONTROLS:
        font = pygame.font.Font("./font.ttf", 20)
        text = font.render("WASD to move", True, "#FFFFFF")
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, 40))
        screen.blit(text, text_rect)
        text = font.render("Shift to sprint", True, "#FFFFFF")
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, 60))
        screen.blit(text, text_rect)

# game loop
while running:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # check if the user pressed a key
        if event.type == pygame.KEYDOWN:
            # check if the user pressed space
            if event.key == pygame.K_SPACE:
                spawn_bullet()

        
    # draw the screen
    draw_screen()
    # handle player movement
    handle_movement()
    # handle bullets
    handle_bullets()


    # render the screen
    pygame.display.flip()
    dt = clock.tick(60) / 1000 # limits FPS to 60

pygame.quit()