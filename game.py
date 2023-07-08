# Example file showing a basic pygame "game loop"
import pygame
import math
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
ROTATION_SPEED = 100
POINTS = 0
POINT_MULTIPLIER = 1
CURR_ANGLE = 0

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
    global CURR_ANGLE
    global POINT_MULTIPLIER
    POINT_MULTIPLIER += 0.1
    angle_step = 360 // 4
    current_angle = CURR_ANGLE
    # for angle in range(0, 360, angle_step):
    #     bullet_dir = pygame.Vector2(1, 0).rotate(angle)
    #     bullet_pos = player_pos + bullet_dir * (PLAYER_RADIUS + 10)
    #     bullet = Bullet(bullet_pos, bullet_dir * BULLET_SPEED, 3)
    #     bullets.append(bullet)
    for i in range(4):
        bullet_dir = pygame.Vector2(1, 0).rotate(current_angle)
        bullet_pos = player_pos + bullet_dir * (PLAYER_RADIUS + 10)
        bullet = Bullet(bullet_pos, bullet_dir * BULLET_SPEED, 3, current_angle)
        bullets.append(bullet)
        current_angle += angle_step
        current_angle %= 360
        bullet.rotate(math.radians(current_angle))
        CURR_ANGLE += ROTATION_SPEED * dt

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
    global POINTS
    if check_bounds():
        return
    keys = pygame.key.get_pressed()
    # check if a movement key is pressed
    if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
        SHOW_CONTROLS = False
        POINTS += len(bullets) * POINT_MULTIPLIER
        if keys[pygame.K_w]:
            if check_sprint():
                player_pos.y -= 500 * dt
            else: 
                player_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            if check_sprint():
                player_pos.y += 500 * dt
            else:
                player_pos.y += 300 * dt
        if keys[pygame.K_a]:
            if check_sprint():
                player_pos.x -= 500 * dt
            else:
                player_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            if check_sprint():
                player_pos.x += 500 * dt
            else:
                player_pos.x += 300 * dt










    
# draw the screen, border, and player
def draw_screen():
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, screen.get_width(), screen.get_height()), BORDER_WIDTH)
    pygame.draw.circle(screen, BORDER_COLOR, player_pos, PLAYER_RADIUS)
    text = "POINTS: " + str(round(POINTS, 1))
    font = pygame.font.Font("./font.ttf", 20)
    text = font.render(text, True, TEXT_COLOR)
    screen.blit(text, (20, 20))

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