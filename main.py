import random
import os

import pygame
from pygame.constants import QUIT, K_ESCAPE, K_s, K_w, K_a, K_d

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 700
WIDTH = 1200

FONT = pygame.font.SysFont("Verdana", 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load("Art/background.png"), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 2

PLAYER_IMAGE_PATH = "Art/Player"
PLAYER_IMAGES = os.listdir(PLAYER_IMAGE_PATH)

print(PLAYER_IMAGES)

player_size = (20, 20)
player = pygame.image.load("Art/player.png").convert_alpha()
player_rect = player.get_rect()
player_speed = 2
player_move_down = [0, player_speed]
player_move_up = [0, -player_speed]
player_move_right = [player_speed, 0]
player_move_left = [-player_speed, 0]


def create_enemy():
    enemy_size = (60, 30)
    enemy = pygame.transform.scale(
        pygame.image.load("Art/enemy.png").convert_alpha(), enemy_size
    )
    enemy_rect = pygame.Rect(WIDTH + 60, random.randint(30, HEIGHT - 30), *enemy_size)
    enemy_move = [random.randint(-6, -4), 0]
    return [enemy, enemy_rect, enemy_move]


def create_bonus():
    bonus_size = (80, 120)
    bonus = pygame.transform.scale(pygame.image.load("Art/bonus.png"), bonus_size)
    bonus_rect = pygame.Rect(random.randint(30, WIDTH - 110), -120, *bonus_size)
    bonus_move = [0, random.randint(1, 3)]
    return [bonus, bonus_rect, bonus_move]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []

score = 0

player_image_index = 0

playing = True

while playing:
    FPS.tick(120)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT or keys[K_ESCAPE]:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(
                os.path.join(PLAYER_IMAGE_PATH, PLAYER_IMAGES[player_image_index])
            )
            player_image_index += 1
            if player_image_index >= len(PLAYER_IMAGES):
                player_image_index = 0

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    if keys[K_s] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_w] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_d] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_a] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
