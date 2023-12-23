import random
import sys

import pygame

# 1- CREATE WINDOW
pygame.init()
# - give or window a name
pygame.display.set_caption("RunX")
# control the framerate
clock = pygame.time.Clock()
# 2- DISPLAY SURFACE
screen = pygame.display.set_mode((900, 500))


def score_board():
    global sc
    sc = pygame.time.get_ticks() - start_time
    score_surface = pygame.font.Font("fonts/PixieFont.ttf", 40)
    score_surface = score_surface.render(f" Score: {sc // 1000}", False, (64, 64, 64)).convert()
    score_rect = score_surface.get_rect(topleft=(320, 50))
    screen.blit(score_surface, score_rect)
    return sc // 1000


def game_start(x='RUNX GAME', score=0, played=False):
    text_surface = pygame.font.Font("fonts/PixieFont.ttf", 60)
    text_surface = text_surface.render(x, False, (200, 90, 104)).convert()
    text_rect = text_surface.get_rect(topleft=(250, 40))
    screen.blit(text_surface, text_rect)

    text_surface2 = pygame.font.Font("fonts/PixieFont.ttf", 30)
    text_surface2 = text_surface2.render(" PRESS 'SPACE' TO PLAY", False, (84, 104, 164)).convert()
    text_rect2 = text_surface2.get_rect(topleft=(255, 120))
    screen.blit(text_surface2, text_rect2)

    text_surface3 = pygame.font.Font(None, 30)
    text_surface3 = text_surface3.render(f"Your score is : {score}", False, (44, 84, 64)).convert()
    text_rect3 = text_surface3.get_rect(topleft=(340, 170))
    if played:
        screen.blit(text_surface3, text_rect3)


def stand_board(lose=False):
    player_stand = pygame.image.load("images/stand_player.png")
    player_stand_rect = player_stand.get_rect(midtop=(420, 210))
    screen.blit(player_stand, player_stand_rect)

    snail_stand = pygame.image.load("images/stand_snail.png")
    snail_stand_rect = snail_stand.get_rect(midtop=(300, 330))
    if lose:
        screen.blit(snail_stand, snail_stand_rect)


# regular surfaces
full_surface = pygame.image.load("images/full.jpg").convert()

start_time = 0
snail_surface = pygame.image.load("images/snail.png").convert_alpha()
snail_rect = snail_surface.get_rect(bottomright=(800, 390))

player_surface = pygame.image.load("images/player.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom=(90, 390))

gravity = 0
grounded = True
is_game_active = False
h_msg = True
score = 0
played = False
lose = False

obstacle_list_rect = []
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 900)

# 3- make the window working till we exit it
while True:
    # 4- when we exit our window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and grounded:
            gravity = -20

        if event.type == pygame.KEYDOWN and grounded:
            if event.key == pygame.K_SPACE:
                gravity = -20
        if not is_game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_game_active = True
                snail_rect.left = 900
                start_time = pygame.time.get_ticks()

    if is_game_active:
        screen.blit(full_surface, (0, 0))
        # as we have a variable here, so we put it inside while
        score_board()
        score = score_board()

        # snail
        if snail_rect.right <= 0: snail_rect.left = random.randint(900, 1500)
        snail_rect.x -= 6
        screen.blit(snail_surface, snail_rect)

        # player
        gravity += 0.83
        player_rect.y += gravity
        if player_rect.bottom < 390:
            grounded = False
        else:
            grounded = True
        if player_rect.bottom >= 390: player_rect.bottom = 390
        screen.blit(player_surface, player_rect)

        # collision between rect
        if player_rect.colliderect(snail_rect):
            is_game_active = False
            h_msg = False
            played = True
            lose = True

            # collision using mouse
        # mouse_pos = pygame.mouse.get_pos()
        # if player_rect.collidepoint(mouse_pos):
        #     print("mouse")

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print("jump")

    else:
        screen.blit(full_surface, (0, 0))
        if not h_msg:
            game_start("GAME OVER", score, played)
        else:
            game_start()  # msg init
        stand_board(lose)  # stand surfaces

    # 5- update our window
    pygame.display.update()
    # - the framerate of the game is 60
    clock.tick(60)
