import pygame

SHOW_CONTROLS = True
BORDER_WIDTH = 20
PLAYER_RADIUS = 7
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FONT = "utils/font.ttf"
FONT_COLOR = "#bc7ad6"
BG_COLOR = "#443554"
BORDER_COLOR = "#19151c"
ROTATION_SPEED = 500
POINTS = 0
POINT_MULTIPLIER = 0.9 # 1.0 when game begins
CURR_ANGLE = 0
LIVES = 5
MAX_POINTS = 1000
INVINCIBLE_TIME = 1500
INVINCIBLE_TIMER = 0
INVINCIBLE = False
SHAKE_DURATION = 100
SHAKE_MAG = 7
SHAKE_TIMER = 0
SHAKE_OFFSET = pygame.Vector2(0, 0)
BULLET_SPEED = 300