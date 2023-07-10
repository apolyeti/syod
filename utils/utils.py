import pygame
import math
import random

# import bullet class
from utils.bullet import Bullet
# import globals
from utils.globals import *


# set up display and player position for util functions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
# set up bullets list and dt for util functions
bullets = []
dt = 0


# for dt to update in game.py
def update_dt(new_dt):
    global dt
    dt = new_dt

# check if player has hit the border or not
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

# draw 4 bullets surrounding player
def spawn_bullet():
    global CURR_ANGLE, POINT_MULTIPLIER, MAX_POINTS
    POINT_MULTIPLIER += 0.1
    MAX_POINTS *= 1.5 * POINT_MULTIPLIER
    angle_step = 360 // 4
    current_angle = CURR_ANGLE

    for _ in range(4):
        bullet_dir = pygame.Vector2(1, 0).rotate(current_angle)
        bullet_pos = player_pos + bullet_dir * (PLAYER_RADIUS + 10)
        bullet = Bullet(bullet_pos, bullet_dir * BULLET_SPEED, 3, current_angle)
        bullets.append(bullet)
        current_angle += angle_step
        current_angle %= 360
        bullet.rotate(math.radians(current_angle))
        CURR_ANGLE += ROTATION_SPEED * dt

# move bullets and check if they have hit the player
def handle_bullets():
    global LIVES, INVINCIBLE, INVINCIBLE_TIME, INVINCIBLE_TIMER, SHAKE_TIMER, SHAKE_MAG
    for bullet in bullets:
        bullet.move(dt)
        bullet.check_bounds(screen)
        if not INVINCIBLE and bullet.check_collision(player_pos):
            bullets.remove(bullet)
            LIVES -= 1
            SHAKE_MAG += 2
            INVINCIBLE = True
            INVINCIBLE_TIMER = pygame.time.get_ticks()
            SHAKE_TIMER = pygame.time.get_ticks()
            return True if LIVES == 0 else False

        if INVINCIBLE and pygame.time.get_ticks() - INVINCIBLE_TIMER > INVINCIBLE_TIME:
            INVINCIBLE = False

# if shift pressed move faster
def check_sprint():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LSHIFT or pygame.K_RSHIFT]:
        return True
    return False

def handle_movement():
    global SHOW_CONTROLS, POINTS, SHAKE_MAG, SHAKE_OFFSET, SHAKE_TIMER, player_pos
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

# restart game
def reinit():
    global POINTS, POINT_MULTIPLIER, CURR_ANGLE, LIVES, SHAKE_MAG, SHOW_CONTROLS, MAX_POINTS, player_pos
    POINTS = 0
    POINT_MULTIPLIER = 0.9
    CURR_ANGLE = 0
    LIVES = 5
    SHAKE_MAG = 7
    SHOW_CONTROLS = True
    MAX_POINTS = 5000
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    pygame.draw.circle(screen, BORDER_COLOR, player_pos, PLAYER_RADIUS)
    bullets.clear()

    
# draw the screen, border, and player
def draw_screen():
    global SHAKE_MAG, SHAKE_OFFSET, SHAKE_TIMER
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, BORDER_COLOR, (
        SHAKE_OFFSET.x,  # Adjust X position of the border
        SHAKE_OFFSET.y,  # Adjust Y position of the border
        screen.get_width(),  # Adjust the width of the border
        screen.get_height()  # Adjust the height of the border
    ), BORDER_WIDTH)
    pygame.draw.circle(screen, BORDER_COLOR, player_pos + SHAKE_OFFSET, PLAYER_RADIUS)
    text = "POINTS: " + str(round(POINTS))
    font = pygame.font.Font(FONT, 20)
    text = font.render(text, True, FONT_COLOR)
    screen.blit(text, (20, 20))
    text = "LIVES: " + str(LIVES)
    text = font.render(text, True, FONT_COLOR)
    screen.blit(text, (20, 40))

    for bullet in bullets:
        bullet.draw(screen)
    
    if SHOW_CONTROLS:
        font = pygame.font.Font(FONT, 20)
        text = font.render("WASD TO MOVE", True, "#FFFFFF")
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, 40))
        screen.blit(text, text_rect)
        text = font.render("SHIFT TO SPRINT", True, "#FFFFFF")
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, 60))
        screen.blit(text, text_rect)

    if SHAKE_TIMER > 0:
            elapsed_time = pygame.time.get_ticks() - SHAKE_TIMER
            if elapsed_time < SHAKE_DURATION:
                SHAKE_OFFSET = pygame.Vector2(
                    random.uniform(-SHAKE_MAG, SHAKE_MAG),
                    random.uniform(-SHAKE_MAG, SHAKE_MAG)
                )
            else:
                SHAKE_OFFSET = pygame.Vector2(0, 0)
                SHAKE_TIMER = 0

# game over screen        
def draw_game_over():
    screen.fill(BG_COLOR)
    font = pygame.font.Font(FONT, 30)
    text = font.render("GAME OVER", True, FONT_COLOR)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text, text_rect)
    text = font.render("POINTS: " + str(round(POINTS)), True, FONT_COLOR)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30))
    screen.blit(text, text_rect)
    # make it so that the play again text flashes
    text = font.render("RETRY?", True, FONT_COLOR)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80))
    screen.blit(text, text_rect)
    show_text = True
    if pygame.time.get_ticks() % 1000 < 500:
        show_text = False
    if show_text:
        text = font.render("PRESS SPACE", True, FONT_COLOR)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 110))
        screen.blit(text, text_rect)
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        reinit()
        return True
    pygame.display.flip()
    return False