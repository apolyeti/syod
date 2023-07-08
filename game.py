# Example file showing a basic pygame "game loop"
import pygame
import math
from bullet import Bullet

# set up constants
SHOW_CONTROLS = True
BORDER_WIDTH = 20
PLAYER_RADIUS = 7
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TEXT_COLOR = "#bc7ad6"
BG_COLOR = "#443554"
BORDER_COLOR = "#19151c"
ROTATION_SPEED = 500
POINTS = 0
POINT_MULTIPLIER = 0.9 # 1.0 when game begins
CURR_ANGLE = 0
LIVES = 5
GAME_STATE = "GAME"
MAX_POINTS = 1000
INVINCIBLE_TIME = 1500
INVINCIBLE_TIMER = 0
INVINCIBLE = False

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
    global CURR_ANGLE, POINT_MULTIPLIER, MAX_POINTS
    POINT_MULTIPLIER += 0.1
    MAX_POINTS *= 1.5 * POINT_MULTIPLIER
    angle_step = 360 // 4
    current_angle = CURR_ANGLE
    # for angle in range(0, 360, angle_step):
    #     bullet_dir = pygame.Vector2(1, 0).rotate(angle)
    #     bullet_pos = player_pos + bullet_dir * (PLAYER_RADIUS + 10)
    #     bullet = Bullet(bullet_pos, bullet_dir * BULLET_SPEED, 3)
    #     bullets.append(bullet)
    for _ in range(4):
        bullet_dir = pygame.Vector2(1, 0).rotate(current_angle)
        bullet_pos = player_pos + bullet_dir * (PLAYER_RADIUS + 10)
        bullet = Bullet(bullet_pos, bullet_dir * BULLET_SPEED, 3, current_angle)
        bullets.append(bullet)
        current_angle += angle_step
        current_angle %= 360
        bullet.rotate(math.radians(current_angle))
        CURR_ANGLE += ROTATION_SPEED * dt

def handle_bullets():
    global LIVES, INVINCIBLE, INVINCIBLE_TIME, INVINCIBLE_TIMER
    for bullet in bullets:
        bullet.move(dt)
        bullet.check_bounds(screen)
        if not INVINCIBLE and bullet.check_collision(player_pos):
            bullets.remove(bullet)
            LIVES -= 1
            INVINCIBLE = True
            INVINCIBLE_TIMER = pygame.time.get_ticks()
        


        if bullet.pos[0] <= bullet.radius or bullet.pos[0] >= screen.get_width() - bullet.radius:
            bullet.reflect(pygame.Vector2(1, 0))
        if bullet.pos[1] <= bullet.radius or bullet.pos[1] >= screen.get_height() - bullet.radius:
            bullet.reflect(pygame.Vector2(0, 1))

        if INVINCIBLE and pygame.time.get_ticks() - INVINCIBLE_TIMER > INVINCIBLE_TIME:
            INVINCIBLE = False




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
    global SHOW_CONTROLS, POINTS
    if check_bounds():
        return
    keys = pygame.key.get_pressed()
    # check if a movement key is pressed
    if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
        SHOW_CONTROLS = False
        if POINTS < MAX_POINTS:
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

def reinit():
    global POINTS, POINT_MULTIPLIER, CURR_ANGLE, LIVES, GAME_STATE
    POINTS = 0
    POINT_MULTIPLIER = 0.9
    CURR_ANGLE = 0
    LIVES = 5
    GAME_STATE = "GAME"
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    pygame.draw.circle(screen, BORDER_COLOR, player_pos, PLAYER_RADIUS)
    bullets.clear()

    
# draw the screen, border, and player
def draw_screen():
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, screen.get_width(), screen.get_height()), BORDER_WIDTH)
    pygame.draw.circle(screen, BORDER_COLOR, player_pos, PLAYER_RADIUS)
    text = "POINTS: " + str(round(POINTS))
    font = pygame.font.Font("./font.ttf", 20)
    text = font.render(text, True, TEXT_COLOR)
    screen.blit(text, (20, 20))
    text = "LIVES: " + str(LIVES)
    text = font.render(text, True, TEXT_COLOR)
    screen.blit(text, (20, 40))

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
        
def draw_game_over():
        screen.fill(BG_COLOR)
        font = pygame.font.Font("./font.ttf", 30)
        text = font.render("GAME OVER", True, TEXT_COLOR)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text, text_rect)
        text = font.render("POINTS: " + str(round(POINTS)), True, TEXT_COLOR)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30))
        screen.blit(text, text_rect)
        # make it so that the play again text flashes
        text = font.render("RETRY?", True, TEXT_COLOR)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80))
        screen.blit(text, text_rect)
        show_text = True
        if pygame.time.get_ticks() % 1000 < 500:
            show_text = False
        if show_text:
            text = font.render("PRESS SPACE", True, TEXT_COLOR)
            text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 110))
            screen.blit(text, text_rect)
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            reinit()
        pygame.display.flip()

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

    if GAME_STATE == "GAME": 
        # draw the screen
        draw_screen()
        # handle player movement
        handle_movement()
        # handle bullets
        handle_bullets()
    elif GAME_STATE == "GAME_OVER":
        draw_game_over()

    if LIVES == 0:
        GAME_STATE = "GAME_OVER"




    # render the screen
    pygame.display.flip()
    dt = clock.tick(60) / 1000 # limits FPS to 60

pygame.quit()